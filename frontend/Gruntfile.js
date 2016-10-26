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
                'server/app/*.js'
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
              'server/app/app.module.js',
              'server/app/*.service.js',
              'server/app/*.directive.js',
              'server/app/*.controller.js',
        ],
        dest: 'static/js/app.concat.js'
      }
    }
  });
  // grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  // grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.registerTask('default', ['watch']);
}
