// including plugins
var gulp = require('gulp'), 
uglify = require("gulp-uglify"), 
gutil = require('gulp-util'), 
concat = require('gulp-concat'), 
minifyCss = require("gulp-minify-css"),
fs = require('fs'),
header = require("gulp-header");

var scripts = ['./ldc.js','./ui.js'];

var styles = ['./ldc.css'];

var thirdparty = [
    "./3rdparty/bootstrap.min.css",
    "./3rdparty/gfonts.css",
    "./3rdparty/font-awesome.min.css",
    "./3rdparty/jquery.rateyo.min.css",
];

var getCopyright = function () {
    return fs.readFileSync('./header.txt');
};

gulp.task('build', function () {
    gulp.src(scripts) 
    .pipe(uglify())
    .on('error', function (err) { gutil.log(gutil.colors.red('[Error]'), err.toString()); })
    .pipe(concat('ldc.min.js'))
    .pipe(header(getCopyright()))
    .pipe(gulp.dest('built'));
    gulp.src(styles) 
    .pipe(minifyCss())
    .on('error', function (err) { gutil.log(gutil.colors.red('[Error]'), err.toString()); })
    .pipe(concat('ldc.min.css'))
    .pipe(header(getCopyright()))
    .pipe(gulp.dest('built'));
     gulp.src(thirdparty) 
    .pipe(minifyCss())
    .pipe(concat('3rdparty.min.css'))
    .pipe(gulp.dest('built'));
});

