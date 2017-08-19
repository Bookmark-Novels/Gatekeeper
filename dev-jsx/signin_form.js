import 'whatwg-fetch'
import React from 'react'
import Helmet from 'react-helmet'
import {Input, WorkButton} from './form.js'
import {Alert, Alerts} from './alerts.js'

export class SignInForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      alerts: [],
      working: false
    }
  }

  handleSubmit (e) {
    e.preventDefault()

    var that = this
        // Probably a bad idea to name it this but oh well...
    var alert = function (a) {
      that.setState({
        alerts: [a]
      })
    }

    this.setState({
      working: true
    })

    var payload = new FormData(this.signin_form)

    fetch(gatekeeper.ep.signin, {
      method: 'POST',
      headers: {
        'X-CSRFToken': gatekeeper.csrf_token
      },
      body: payload,
      // Cookies cannot be set by AJAX responses if this is not set.
      credentials: 'same-origin'
    }).then(function (resp) {
      that.setState({
        working: false
      })

      if (!resp.ok) {
        throw new Error()
      }

      return resp.json()
    }).then(function (resp) {
      if (resp.error) {
        alert(resp.error)
      } else {
        if (that.props.location.query.next) {
          window.location.href = that.props.location.query.next
        }

        window.location.href = resp.redirect
      }
    }).catch(function () {
      alert('An unexpected error occurred while processing your request.')
    })
  }

  render () {
    let email = React.createElement(Input, {
      label: 'Email Address',
      type: 'email',
      name: 'email',
      placeholder: 'email@bookmarknovels.com',
      required: true
    })

    let password = React.createElement(Input, {
      label: 'Password',
      type: 'password',
      name: 'password',
      placeholder: 'Super Secret Password',
      required: true
    })

    let alerts = this.state.alerts.map((alert, index) => {
      return <Alert key={index.toString()} type='error'>{alert}</Alert>
    })

    return (
      <div>
        <Helmet title='Bookmark Sign In' />
        <Alerts>
          {alerts}
        </Alerts>
        <aside id='gatekeeper-modal'>
          <form method='POST' id='gatekeeper-form' onSubmit={this.handleSubmit.bind(this)} ref={(c) => { this.signin_form = c }}>
            <header>
              <h1>Sign In to Bookmark</h1>
            </header>
            {email}
            {password}
            <div id='gatekeeper-form-bottom'>
              <div id='gatekeeper-form-links' className='vertical-align'>
                <span>
                  <a href={`${gatekeeper.sitemap.register}`}>Create Account</a>
                  <span className='gray'> / </span>
                  <a href={`${gatekeeper.sitemap.forgot_password}`}>Forgot Password</a>
                </span>
              </div>
              <div id='gatekeeper-form-buttons' className='vertical-align'>
                {
                    /*
                    <span>
                        <input type="checkbox" name="remember" id="remember" />
                        &nbsp;
                        <label htmlFor="remember">Remember Me</label>
                    </span>
                    */
                }
                <WorkButton className='btn-primary' type='submit' name='login' working={this.state.working} >
                  Sign In
                </WorkButton>
              </div>
            </div>
          </form>
        </aside>
      </div>
    )
  }
}
