let mix = require('laravel-mix');

mix
    .js('resources/js/app.js', 'js')
    .js('resources/js/query.js', 'js')
    .sass('resources/sass/app.scss', 'css')
    .setPublicPath('static')
    .browserSync('localhost:5000');