$(document).ready(function() {
  $('#share-button').click(share_click);
});

function get_feed_url(image_url) {
  feed_url = feed_url_base + '&picture=' + escape(image_url);
  return feed_url
}

share_click = function(event) {
  event.preventDefault();

  // get top text, bottom text, meme id
  top_text = $('#fm-top-text').val();
  bottom_text = $('#fm-bottom-text').val();
  meme_id = 'fry';

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
