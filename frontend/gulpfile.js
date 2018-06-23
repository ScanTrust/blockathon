'use strict';

var gulp = require('gulp');
var rename = require("gulp-rename");
var util = require('gulp-util');

gulp.task('config', function() {

  gulp.src(['./env/' + (util.env.deploy ? util.env.deploy : 'staging') + '.js'])
    .pipe(rename('config.js'))
    .pipe(gulp.dest('src/'));

});
