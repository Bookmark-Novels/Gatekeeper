import React from 'react'
import ReactDOM from 'react-dom'
import {Router, Route, browserHistory} from 'react-router'
import {SignInForm} from './signin_form.js'
import {RegisterForm} from './register_form.js'
import {PageNotFound} from './page_not_found.js'
import {NavBar} from './navbar.js'

// import { ForgotPasswordForm } from './forgot_password.js';

class Gatekeeper extends React.Component {
  render () {
    return (
      <div>
        <aside id='gatekeeper-top-bar'>
          <NavBar />
        </aside>
        <div id='gatekeeper-modal-wrapper'>
          {this.props.children}
        </div>
      </div>
    )
  }
}

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path='/' component={Gatekeeper}>
      <Route path={gatekeeper.sitemap.register} component={RegisterForm} />
      <Route path={gatekeeper.sitemap.signin} component={SignInForm} />
      <Route path='*' component={PageNotFound} />
    </Route>
  </Router>
), document.querySelector('main'))

/*
<Route path={ gatekeeper.sitemap.forgot_password } component={ ForgotPasswordForm } />
*/
