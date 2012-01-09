meme_type = '';
baked = false;
image_url = '';

childflag = false;
child = undefined;

$(document).ready(function() {

  $('.fm-top-text').each(function() {
    $(this).keyup(function() {
      meme_id = $(this).attr('id').substring(0, $(this).attr('id').indexOf('-'));
      updateMemeText(meme_id);
    });
  });

  $('.fm-bottom-text').each(function() {
    $(this).keyup(function() {
      meme_id = $(this).attr('id').substring(0, $(this).attr('id').indexOf('-'));
      updateMemeText(meme_id);
    });
  });

});


updateMemeText = function(meme_id, redraw) {
  if (redraw == undefined) {
    redraw = true;
  }

  canvas_id = meme_id + '-canvas';
  top_id = '#' + meme_id + '-top';
  bottom_id = '#' + meme_id + '-bottom';

  canvas = document.getElementById(canvas_id);

  top_text = $(top_id).val();
  bottom_text = $(bottom_id).val();

  if (top_text == 'top text') top_text = '';
  if (bottom_text == 'bottom text') bottom_text = '';

  writeMemeText(top_text, bottom_text, canvas, redraw);
}



bake = function(meme_id) {
  console.log('baking...');
  canvas_id = meme_id + '-canvas';
  image_id = meme_id + '-image';
  spinner_id = '#' + meme_id + ' img.loading';
  share_id = '#' + meme_id + ' .share-button img.share-image';

  canvas = document.getElementById(canvas_id);
  image = document.getElementById(image_id);

  context = getContextForText(canvas);

  context.drawImage(image, 0, 0);
  updateMemeText(meme_id, false);

  var imageBytes = canvas.toDataURL("image/jpeg");

  data = {
    'image': imageBytes,
    'meme_type': meme_type,
  }

  $(spinner_id).css('display', 'block');
  $(share_id).css('display', 'none');

  child = window.open(window.location.origin + '/fbshare', 'child', 'height=400,width=625,scrollbars');

  $.ajax({
    url: 'bake',
    type: 'post',
    data: data,
    success: function(response) {
      image_url = response;
      send_child_to_facebook();  
    },
  });
};

send_child_to_facebook = function() {
  if (childflag == false) {
    setTimeout('send_child_to_facebook()', 1000);
    return;
  } else {
    child.location = 'https://www.facebook.com/sharer.php?u=' + escape(image_url);
    return;
  }
}

childopen = function() {
  if (childflag == true) {
    window.location = image_url;
    child.close();
  } else {
    childflag = true;
  }
}

// buttsecks the canvas context so we can write text properly
getContextForText = function (canvas) {
  ctx = canvas.getContext('2d');

  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  console.log(canvas.height);
  ctx.fontsize = canvas.height / 10;
  ctx.font = ctx.fontsize + "px MemeImpact";
  ctx.textBaseline = "middle";
  return ctx;
}

 
writeMemeText = function(top_text,bottom_text,canvas,redraw) {
  ctx = getContextForText(canvas);

  if (redraw !== false) {
    // clear canvas and redraw
    ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);
  }
 
  // make nice offsets for line spacing and vertical margin
  var v_off = ctx.fontsize;
  console.log(v_off);
  //v_off = 60;

  top_text = formatText(top_text, ctx);
  if (top_text) {
    for (var i = 0; i < top_text.length; i++) {
      ctx.fillText(top_text[i],ctx.canvas.width/2,v_off+v_off*i);
      ctx.strokeText(top_text[i],ctx.canvas.width/2,v_off+v_off*i);
    }
  }

  bottom_text = formatText(bottom_text, ctx);
  if (bottom_text) {
    for (var i = 0; i < bottom_text.length; i++) {
      ctx.fillText(bottom_text[i],ctx.canvas.width/2,ctx.canvas.height-v_off-v_off*(bottom_text.length-1-i));
      ctx.strokeText(bottom_text[i],ctx.canvas.width/2,ctx.canvas.height-v_off-v_off*(bottom_text.length-1-i));
    }
  }
}
 
 
formatText = function(text, ctx) {
    if (!text) {
        return;
    }
 
    var text_width = ctx.measureText(text).width;
 
    if (text_width >= ctx.canvas.width) {
        // begin splitting lines
 
        // we want a 2D array of words
        var out = breakTextArray(text.split(" "), ctx);
 
        // merge rows back into strings
        for (var i = 0; i < out.length; i++) {
            out[i] = out[i].join(" ");
        }
 
        return out;
    } else {
        return [text];
    }
}
 
// break an array words into more rows until they fit
breakTextArray = function(ta, ctx) {
    var start, end;
    var rowwidth = ctx.canvas.width;
    var spacewidth = ctx.measureText(" ").width;
 
    start = 0;
    end = 0;
 
    var last = ta.length;
 
    var out = [];
 
    var cur_length = 0;
 
    while (end < last) {
        cur_length += ctx.measureText(ta[end]).width;
 
        if (cur_length >= rowwidth) {
            // move everything from before now into a row
            if (start == end) {
                // handle case of single word longer than row
                out.push([ta[start]]);
 
                start++;
                end++;
 
                cur_length = 0;
            } else {
                out.push(ta.slice(start, end));
                start = end;
                
                cur_length = 0;
            }
 
        } else {
            // we've advanced by a word. account for space.
            end++;
            cur_length += spacewidth;
        }
    }
 
    if (start != end) {
        out.push(ta.slice(start,end));
    }
 
    return out;
}
