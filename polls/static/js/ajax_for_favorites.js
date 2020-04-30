const add_to_favorites_url = '/favorites/add/';
const remove_from_favorites_url = '/favorites/remove/';
const favorites_api_url = '/favorites/api/';
const added_to_favorites_class = 'added';


function add_to_favorites(){
    $('.add-to-favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const type = $(el).data('type');
            const id = $(el).data('id');

            if( $(e.target).hasClass(added_to_favorites_class) ) {

                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(added_to_favorites_class)
                    }
                })
            } else {

                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data:{
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(added_to_favorites_class)
                        // get_session_favorites_statistics()
                    }
                })
            };
        })
    })
};


function get_session_favorites() {
    // get_session_favorites_statistics()

    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {
                $('.add-to-favorites').each((index, el) => {
                    const type = $(el).data('type')
                    const id = $(el).data('id')

                    if ( json[i].type == type && json[i].id == id ){
                        $(el).addClass(added_to_favorites_class)
                    }
                })
            }
        }
    })
}

$(document).ready(function() {
    add_to_favorites()
    get_session_favorites()
})
