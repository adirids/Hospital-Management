$(document).ready(function() {
  $.post(
    "/scoreset",
    function(data) {
      for (let i = 0; i < data.length; i++) {
        data[i];
        $("#scoretable").append(
          '<tr>          <td class="data">' +
            (i + 1) +
            '</td>          <td class="data">' +
            data[i].fname +
            '</td>          <td class="data">' +
            data[i].score +
            "</td>      </tr>"
        );
      }
    },
    "json"
  );
  /*$.getJSON('/scoreset',function(data){
    for (var i = 0; i < data.length; i++) {
      data[i];
      $('#scoretable').append('<tr>          <td class="data">'+(i+1)+'</td>          <td class="data">'+data[i].fname+'</td>          <td class="data">'+data[i].score+'</td>      </tr>');
    }
  });*/
});
