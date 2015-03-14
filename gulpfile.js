(function () {
    var gulp = require("gulp"),
        changed = require("gulp-changed"),
        jshint = require("gulp-jshint"),
        jshintstylish = require("jshint-stylish"),
        concat = require("gulp-concat"),
        uglify = require("gulp-uglify"),
        rename = require("gulp-rename"),
        imagemin = require("gulp-imagemin"),
        clean = require("gulp-clean"),
        minifyhtml = require("gulp-minify-html"),
        autoprefixer = require("gulp-autoprefixer"),
        minifyCSS = require("gulp-minify-css"),
        copy = require("gulp-copy"),
        runSequence = require("run-sequence");

    var devSrc = "./dev";
    var buildSrc = "./build";

    gulp.task("images", function () {
        var imgSrc = devSrc + "/assets/**/*",
            imgDst = buildSrc + "/assets";

        return gulp.src(imgSrc)
            .pipe(changed(imgDst))
            .pipe(imagemin())
            .pipe(gulp.dest(imgDst));
    });

    gulp.task("lint", function () {
        return gulp.src(devSrc + "/js/*.js")
            .pipe(jshint())
            .pipe(jshint.reporter(jshintstylish));
    });

    gulp.task("scripts", function () {
        return gulp.src(devSrc + "/js/*.js")
            .pipe(concat("all.js"))
            .pipe(rename("all.min.js"))
            .pipe(uglify())
            .pipe(gulp.dest(buildSrc + "/js"));
    });

    gulp.task("minify-css", function () {
        return gulp.src(devSrc + "/css/**/*")
            .pipe(concat("all.css"))
            .pipe(rename("all.min.css"))
            .pipe(minifyCSS())
            .pipe(gulp.dest(buildSrc + "/css"));
    });

    gulp.task("watch", function () {
        gulp.watch(devSrc + "/js/*.js", ["lint", "scripts"]);
    });

    gulp.task("copy", function () {
        return gulp.src(
            [devSrc + "/**/*",
                "!" + devSrc + "/assets/**/*",
                "!" + devSrc + "/js/**/*",
                "!" + devSrc + "/css/**/*"])
            .pipe(changed(buildSrc))
            .pipe(gulp.dest(buildSrc));
    });

    gulp.task("build", ["copy", "images", "scripts", "minify-css"]);

    gulp.task('default', function () {
        runSequence("lint", "build", "watch");
    });
}());