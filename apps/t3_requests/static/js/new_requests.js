var NEW_REQUESTS = 0,
    CHANGED = false,
    FOCUSED = true;
setInterval(function(){
    $.ajax({
        url: window.location['pathname'],
        data: {'order': $('[name="order"]:checked').val()},
        success: function(data){
            $( data['requests'].reverse() ).each(function(index){
                if ( $("p[data-object-id=" + this.id + "]").length > 0){
                    return true
                } else {
                    NEW_REQUESTS += 1;
                };
            });
            if (NEW_REQUESTS || CHANGED){
                CHANGED = false;
                $('.requests').empty();
                $( data['requests'].reverse() ).each(function(index){
                    $('.requests').append(
                        "<p data-object-id=" + this.id + ">" + (index + 1) + ". priority: " + 
                    '<button onclick="changePriority(this, -1)">-</button>' + 
                    this.priority + '<button onclick="changePriority(this, 1)">+</button> ' + 
                    this.created + ' ' + this.method + ' ' + this.path + ' ' + this.query + 
                    ' by ' + this.user + "</p>"
                    );
                });
            }
            var title = $('title').text();
            if (NEW_REQUESTS && !FOCUSED) {
                if (title[0] != '('){
                    title = '(' + NEW_REQUESTS + ') ' + title;
                } else {
                    title = title.replace(/\(\d+\)/, '(' + NEW_REQUESTS + ')');
                };
                $('title').text(title);
            } else {
                NEW_REQUESTS = 0;
                $('title').text('Last requests');
            };
        },
        dataType: "json"
    });
}, 3000);
$(window).focus(function(){
    $('title').text('Last requests');
    NEW_REQUESTS = 0;
    FOCUSED = true;
}).blur(function(){
    FOCUSED = false;
});
$('[name="order"]').on('change', function(){
    $.ajax({
        url: window.location['pathname'],
        data: {'order': $('[name="order"]:checked').val()},
        success: function(data){
            NEW_REQUESTS = 0;
            FOCUSED = true;
            $('.requests').empty();
            $( data['requests'] ).each(function(index){
                $('.requests').append(
                    "<p data-object-id=" + this.id + ">" + (index + 1) + ". priority: " + 
                    '<button onclick="changePriority(this, -1)">-</button>' + 
                    this.priority + '<button onclick="changePriority(this, 1)">+</button> ' + 
                    this.created + ' ' + this.method + ' ' + this.path + ' ' + this.query + 
                    ' by ' + this.user + "</p>"
                );
            });
        },
        dataType: "json"
    });
});
function changePriority(elem, value){
    var priority = $(elem).parent().get(0).childNodes[2].textContent;
    if ( +priority + value > 9 || +priority + value < 1 ) {
        return
    }    
    var id = $(elem).parent().attr('data-object-id');
    $.ajax({
        url: changePriorityUrl,
        data: {id: id, value: value},
        success: function(data){
            $(elem).parent().get(0).childNodes[2].textContent = +priority + value;
            CHANGED = true;
        },
        dataType: "json"
    });
}