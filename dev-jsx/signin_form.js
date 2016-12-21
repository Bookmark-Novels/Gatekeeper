import React from 'react';
import { Link } from 'react-router';
import { Input } from './input.js';

export class SignInForm extends React.Component {
    constructor(props){
        super(props);
        this.email = React.createElement(Input, {
            label: 'Email Address',
            type: 'email',
            name: 'email',
            id: 'gatekeeper-form-email',
            placeholder: 'email@bookmarknovels.com'
        });

        this.password = React.createElement(Input, {
            label: 'Password',
            type: 'password',
            name: 'password',
            id: 'gatekeeper-form-password',
            placeholder: 'Super Secret Password'
        });
    }

    render(){
        return (
            <form method="POST" id="gatekeeper-form">
                <header>
                    <h1>Sign in to Bookmark</h1>
                </header>
                <input type="hidden" name="csrf_token" value={ gatekeeper.csrf_token } />
                { this.email }
                { this.password }
                <div id="gatekeeper-form-bottom">
                    <div id="gatekeeper-form-links" className="vertical-align">
                        <span>
                            <Link to="/signup">Create Account</Link>
                            <span className="gray"> / </span>
                            <Link to="/forgot-password">Forgot Password</Link>
                        </span>
                    </div>
                    <div id="gatekeeper-form-buttons" className="vertical-align">
                        <span>
                            <input type="checkbox" name="remember" id="remember" />
                            <label htmlFor="remember">Remember Me</label>
                        </span>
                        <button className="btn-primary" type="submit" name="login">Sign In</button>
                    </div>
                </div>
            </form>
        );
    }
}
