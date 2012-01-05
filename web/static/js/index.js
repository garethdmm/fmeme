$(document).ready(function() {
  $('#share-button').click(bake);
  $('.share-button').click(share_click);
  $('.fm-grid-square').click(grid_square_click);
  $('a.back-button').click(back_button_click);
});

function get_feed_url(image_url) {
  feed_url = feed_url_base + '&link=' + escape(image_url);
  return feed_url;
}

resize_canvas = function(meme_id) {
  canvas_id = meme_id + '-canvas';
  image_id = meme_id + '-image';

  canvas = document.getElementById(canvas_id);
  image = document.getElementById(image_id);

  canvas.width = image.naturalWidth;
  canvas.height = image.naturalHeight;
}

back_button_click = function(event) {
  event.preventDefault();
  // get the id
  meme_id = $(this).attr('id').substring(0, $(this).attr('id').indexOf('-'));

  // set the div as neutral
  $('div#' + meme_id).removeClass('active');
  $('div#' + meme_id).addClass('closed');

  // set all other divs as neutral
  $('div.fm-grid-square.inactive').removeClass('inactive');
  $('div.fm-grid-square').addClass('neutral');
}

grid_square_init = function() {
  $(this).click(grid_square_click);
}

grid_square_click = function(event) {
  if ($(this).hasClass('closed')) {
    $(this).removeClass('closed')
    return;
  } else if ($(this).hasClass('active')) {
    return;
  }

  $('body').animate({
    scrollTop: '0px',
  }, 400);
    
  meme_id = $(this).attr('id');
  div_id = 'div#' + meme_id;
  canvas_id = '#' + meme_id +'-canvas';
  image_id = div_id + ' img.meme-image';
  top_id = '#' + meme_id + '-top';
  
  // update the global
  meme_type = meme_id;

  // add class inactive to all others
  $('div.fm-grid-square.neutral').removeClass('neutral');
  $('div.fm-grid-square').addClass('inactive');

  // add class active
  $(this).removeClass('inactive');
  $(this).addClass('active');

  $(canvas_id).height($(image_id).height());
  $(canvas_id).width($(image_id).width());
  $(canvas_id).offset($(image_id).offset());

  resize_canvas(meme_id);

  $(top_id).focus();
}

share_click = function(event) {
  event.preventDefault();

  // get the meme id
  meme_id = $(this).attr('id').substring(0, $(this).attr('id').indexOf('-'));
  bake(meme_id);
  return;

  div_id = 'div#' + meme_id;

  // get top text, bottom text
  top_text = $(div_id + ' .fm-top-text').val();
  bottom_text = $(div_id + ' .fm-bottom-text').val();

  data = {
    'toptext': top_text,
    'bottomtext': bottom_text,
    'memeid': meme_id,
  }

  // post to /bake
  $.ajax({
    url: 'bake',
    type: 'post',
    data: data,
    success: function(response) {
      image_url = response;

      // redirect to the appropriate facebook thingy
      top.location.href = get_feed_url(image_url);
    },
  });
}
