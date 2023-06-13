$(document).ready(function() {
    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    function clearForm() {
        $('#musicForm').attr('action', '/music');
        $('#formTitle').text('Add a new music');
        $('#musicId').val('');
        $('#title').val('');
        $('#artist').val('');
        $('#release_year').val('');
        $('#genre').val('');
        $('#track_list').val('');
    }

    function fetchMusics(trackListFilter = null) {
        $.get('/musics', {track_list_filter: trackListFilter}, function(musics) {
            var musicList = $('#musicList');
            musicList.empty();
            for (var i = 0; i < musics.length; i++) {
                var music = musics[i];
                var musicElement = $('<div></div>')
                    .addClass('col-sm-6 col-md-4 col-lg-3')
                    .append('<div class="card"><div class="card-body"><h5 class="card-title">' + music.title + '</h5><h6 class="card-subtitle mb-2 text-muted">' + music.artist + '</h6><p class="card-text">Released in ' + music.release_year + '</p><p class="card-text">Genre: ' + music.genre + '</p><p class="card-text">' + music.track_list + '</p><button class="btn btn-primary updateButton" data-id="' + music.id + '">Update</button><button class="btn btn-danger deleteButton" data-id="' + music.id + '">Delete</button></div></div>');
                musicList.append(musicElement);
            }
            $('.updateButton').click(function() {
                var musicId = $(this).data('id');
                $.get('/music/' + musicId, function(music) {
                    $('#musicForm').attr('action', '/music/' + musicId);
                    $('#formTitle').text('Update music');
                    $('#musicId').val(music.id);
                    $('#title').val(music.title);
                    $('#artist').val(music.artist);
                    $('#release_year').val(music.release_year);
                    $('#genre').val(music.genre);
                    $('#track_list').val(music.track_list);
                });
            });
            $('.deleteButton').click(function() {
                var musicId = $(this).data('id');
                $.ajax({
                    url: '/music/' + musicId,
                    type: 'DELETE',
                    success: function(result) {
                        fetchMusics();
                        clearForm();
                    }
                });
            });
        });
    }
    fetchMusics();

    $('#musicForm').submit(function(e) {
        e.preventDefault();

        var url = $(this).attr('action');
        var method = 'POST';
        if (url.startsWith('/music/')) {
            method = 'PUT';
        }

        $.ajax({
            url: url,
            type: method,
            data: JSON.stringify($(this).serializeObject()),
            contentType: 'application/json',
            success: function(result) {
                fetchMusics();
                clearForm();
            }
        });
    });

    $('#clearButton').click(function() {
        clearForm();
    });

    $('#trackListFilter').on('input', function() {
        var trackListFilter = $(this).val();
        fetchMusics(trackListFilter);
    });
});
