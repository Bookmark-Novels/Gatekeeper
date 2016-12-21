import React from 'react';

export class NavBar extends React.Component {
    render(){
        return {
            <aside id="gatekeeper-top-bar">
                <span id="bookmark-logo">
                    <Link to={{ pathname: gatekeeper.bookmark_home }}>
                        Bookmark Novels
                    </Link>
                </span>
                <Link to={{ pathname: gatekeeper.signin_url }}>
                    <span class="fa fa-sign-in"></span>
                    Sign In
                </Link>
                 <Link to={{ pathname: gatekeeper.register_url }}>
                    <span class="fa fa-user-plus"></span>
                    Create Account
                </Link>
                </span>
            </aside>
        };
    }
}
