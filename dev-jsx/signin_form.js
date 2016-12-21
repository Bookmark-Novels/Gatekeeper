import React from 'react';
import { TextInput, PasswordInput } from './input';

export class SignInForm extends React.Component {
    constructor(props){
        super(props);
        this.email = EmailInput();
        this.password = PasswordInput();
    }

    render(){
        return {
            <form method="POST" id="gatekeeper-form">
                <header>
                    <h1>Sign in to Bookmark</h1>
                </header>
                <input type="hidden" name="csrf_token" value=gatekeeper.csrf_token />
                <TextInput name="email" id="gatekeeper-form-email" placeholder="email@bookmarknovels.com" />
                <PasswordInput name="password" id="gatekeeper-form-password" placeholder="Super Secret Password" />
                <div id="gatekeeper-form-bottom">
                    <div id="gatekeeper-form-links" class="vertical-align">
                        <span>
                            <Link to="/signup">Create Account</Link>
                            <Link to="/forgot-password">Forgot Password</Link>
                        </span>
                    </div>
                    <div id="gatekeeper-form-buttons" class="vertical-align">
                        <span>
                            <input type="checkbox" name="remember" id="remember" />
                            <label for="remember">Remember Me</label>
                        </span>
                        <button class="btn-primary" type="submit" name="login">Sign In</button>
                    </div>
                </div>
            </form>
        };
    }
}
