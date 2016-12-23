import React from 'react';
import Helmet from 'react-helmet';
import { Link } from 'react-router';
import { Input, WorkButton } from './form.js';
import { Alert, Alerts } from './alerts.js';

export class SignInForm extends React.Component {
    handleSubmit(e){
        e.preventDefault();

        this.refs.login_button.disable();

        fetch(gatekeeper.sitemap.login, {
            method: 'POST',
            body: {
                email: this.refs.email.value,
                password: this.refs.password.value,
                remember_me: this.refs.remember_toggle.value
            }
        }).then(function(resp){
            try{
                resp = JSON.loads(resp.text());

                if(resp.error){
                    this.refs.alert(
                        <Alert type="error">
                            resp.error
                        </Alert>
                    );
                }

                location.href = resp.redirect;
            }
            catch(e){
                this.refs.alert(
                    <Alert type="error">
                        An unexpected error occurred while processing your request.
                    </Alert>
                );
            }
        }, function(err){
            this.refs.alert(
                <Alert type="error">
                    An unexpected error occurred while processing your request.
                </Alert>
            );
        });
    }

    render(){
        let email = React.createElement(Input, {
            label: 'Email Address',
            type: 'email',
            name: 'email',
            id: 'gatekeeper-form-email',
            placeholder: 'email@bookmarknovels.com',
            required: true,
            ref: 'email'
        });

        let password = React.createElement(Input, {
            label: 'Password',
            type: 'password',
            name: 'password',
            id: 'gatekeeper-form-password',
            placeholder: 'Super Secret Password',
            required: true,
            ref: 'password'
        });

        return (
            <aside id="gatekeeper-modal">
                <Helmet title="Bookmark Sign In" />
                <Alerts ref="alerts" />
                <form method="POST" id="gatekeeper-form" onSubmit={ this.handleSubmit }>
                    <header>
                        <h1>Sign in to Bookmark</h1>
                    </header>
                    <input type="hidden" name="csrf_token" value={ gatekeeper.csrf_token } />
                    { email }
                    { password }
                    <div id="gatekeeper-form-bottom">
                        <div id="gatekeeper-form-links" className="vertical-align">
                            <span>
                                <Link to={ gatekeeper.sitemap.register }>Create Account</Link>
                                <span className="gray"> / </span>
                                <Link to={ gatekeeper.sitemap.forgot_password }>Forgot Password</Link>
                            </span>
                        </div>
                        <div id="gatekeeper-form-buttons" className="vertical-align">
                            <span>
                                <input type="checkbox" name="remember" id="remember" />
                                &nbsp;
                                <label htmlFor="remember" ref="remember_toggle">Remember Me</label>
                            </span>
                            <WorkButton className="btn-primary" type="submit" name="login" ref="login_button" >
                                Sign In
                            </WorkButton>
                        </div>
                    </div>
                </form>
            </aside>
        );
    }
}
