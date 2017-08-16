module.exports = function (grunt) {
  grunt.initConfig({
    clean: {
      all: {
        src: ['**/.sass-cache', '**/*.pyc', '**/*.map']
      }
    },
    jshint: {
      files: ['dev-js/*.js'],
      options: {
        globals: {
          jQuery: true
        }
      }
    },
    uglify: {
      everything: {
        files: {
          'static/js/gatekeeper.min.js': ['staging/js/jsx.js', 'dev-js/gatekeeper.js']
        }
      },
      dev: {
        files: {
          'static/js/gatekeeper.min.js': ['staging/js/jsx.js', 'dev-js/gatekeeper.js']
        },
        options: {
          mangle: false,
          compress: false
        }
      }
    },
    sass: {
      dist: {
        options: {
          'sourcemap': 'none',
          'noCache': true,
          'style': 'compressed'
        },
        files: {
          'static/css/gatekeeper.min.css': 'dev-css/gatekeeper.scss'
        }
      }
    },
    browserify: {
      dist: {
        options: {
          plugins: ['transform-react-jsx'],
          transform: [['babelify', {presets: ['stage-0', 'es2015', 'react']}]],
          watch: true,
          keepAlive: true
        },
        src: ['dev-jsx/gatekeeper.js'],
        dest: 'staging/js/jsx.js'
      }
    },
    watch: {
      sass: {
        files: 'dev-css/**/*.scss',
        tasks: ['sass']
      },
      js: {
        files: ['dev-js/**/*.js', 'staging/js/*.js'],
        tasks: ['jshint', 'uglify:dev']
      }
    }
  })

  grunt.loadNpmTasks('grunt-browserify')
  grunt.loadNpmTasks('grunt-contrib-clean')
  grunt.loadNpmTasks('grunt-contrib-jshint')
  grunt.loadNpmTasks('grunt-contrib-uglify')
  grunt.loadNpmTasks('grunt-contrib-sass')
  grunt.loadNpmTasks('grunt-contrib-watch')

  grunt.registerTask('default', ['clean', 'jshint', 'browserify', 'uglify', 'sass'])
}
