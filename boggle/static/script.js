$(document).ready( function() {
  $("#shuffle").click(function(event) {
    $.ajax({
      url: $(this).attr("href"),
      success: function(response) {
        var board = response["board"];
        var html = "";

        for (var i = 0; i < board.length; i++) {
          html += "<div class=\"row\">";
          for (var j = 0; j < board[i].length; j++) {
            html += "<div class=\"col-3 rounded border border-white bg-dark display-4 text-center text-white\">";
            html += board[i][j].toUpperCase();
            html += "</div>";
          }
          html += "</div>";
        }

        $("#board").html(html);
      }
    });

    event.preventDefault();
  });

  $("#lookup").submit(function(event) {
    var word = $("#lookup_word").val();

    $.ajax({
      type: $(this).attr("method"),
      url: $(this).attr("action"),
      data: $(this).serialize(),
      success: function(response) {
        var valid = response["status"];
        var html = "";

        if (valid) {
          html += "<span class=\"text-success\">" + word.toLowerCase() + "</span>\n";
        } else {
          html += "<span class=\"text-danger\">" + word.toLowerCase() + "</span>\n";
        }

        $("#result").prepend(html);
      }
    });

    event.preventDefault();
  });
});
