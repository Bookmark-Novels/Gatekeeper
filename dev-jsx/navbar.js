import React from 'react';
import {Link} from 'react-router';

export class NavBar extends React.Component {
    render(){
        return (
            <nav>
                <span id="bookmark-logo">
                    <Link to={{pathname: gatekeeper.bookmark_host}}>
                        Bookmark Novels
                    </Link>
                </span>
                <Link to={{pathname: gatekeeper.sitemap.signin}}>
                    <span className="fa fa-sign-in"></span>
                    &nbsp;
                    Sign In
                </Link>
                 <Link to={{pathname: gatekeeper.sitemap.register}}>
                    <span className="fa fa-user-plus"></span>
                    &nbsp;
                    Create Account
                </Link>
            </nav>
        );
    }
}
