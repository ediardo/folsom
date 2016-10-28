module.exports = function(grunt) {
  grunt.initConfig({
    /**
    sass: {
      dist: {
        options: {
          style: 'expanded'
        },
        files: { 
          'assets/css/main.css': 'scss/main.scss'
        }
      }
    },
    */
    watch: {
      css: {
        files: [
                '../app/*.js'
               ],
        tasks: ['concat']
      }
    },
    concat: {
      options: {
        separator: '\n\n'
      },
      dist: {
        src: [
              '../app/app.module.js',
              '../app/*.directive.js',
              '../app/*.service.js',
              '../app/*.controller.js',
        ],
        dest: 'js/app.concat.js'
      }
    }
  });
  // grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  // grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.registerTask('default', ['watch']);
}
