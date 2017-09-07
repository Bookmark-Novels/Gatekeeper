import 'whatwg-fetch'
import React from 'react'
import Helmet from 'react-helmet'
import {Input, WorkButton} from './form.jsx'
import {Alert, Alerts} from './alerts.jsx'

export class RegisterForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      alerts: [],
      working: false
    }
  }

  handleSubmit (e) {
    e.preventDefault()

    let that = this
    // Probably a bad idea to name it this but oh well...
    let alert = function (a) {
      that.setState({
        alerts: [a]
      })
    }

    this.setState({
      working: true
    })

    let payload = new FormData(this.register_form)

    fetch(gatekeeper.ep.register, {
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
    let name = React.createElement(Input, {
      label: 'Display Name',
      type: 'text',
      name: 'name',
      placeholder: 'Your Name Here',
      required: true
    })

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
        <Helmet title='Bookmark Sign Up' />
        <Alerts>
          {alerts}
        </Alerts>
        <aside id='gatekeeper-modal'>
          <form method='POST' id='gatekeeper-form' onSubmit={this.handleSubmit.bind(this)} ref={(c) => { this.register_form = c }}>
            <header>
              <h1 className='full-width'>Create a Bookmark Account</h1>
              <h2 className='small-width'>Create a Bookmark Account</h2>
            </header>
            <input type='hidden' name='csrf_token' value='{{ csrf_token() }}' />
            {name}
            {email}
            {password}
            <div id='gatekeeper-form-bottom'>
              <div id='bookmark-registration-agreement' className='small vertical-align'>
                <span>
                    By clicking "Create Account", I am willingly acknowledging and accepting the Bookmark <a href={`${gatekeeper.bookmark_host}/tos`}>terms&nbsp;of&nbsp;service</a> and <a href={`${gatekeeper.bookmark_host}/privacy`}>privacy&nbsp;policy</a>.
                </span>
              </div>
              <div id='gatekeeper-form-buttons' className='vertical-align'>
                <WorkButton className='btn-primary' type='submit' name='register' working={this.state.working} >
                    Create&nbsp;Account
                </WorkButton>
              </div>
            </div>
          </form>
        </aside>
      </div>
    )
  }
}
