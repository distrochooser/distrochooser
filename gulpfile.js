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

// task

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
});

