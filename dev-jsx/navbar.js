import React from 'react'
import {Link} from 'react-router'

export class NavBar extends React.Component {
  render () {
    return (
      <nav>
        <span id='bookmark-logo'>
          <a href={`${gatekeeper.bookmark_host}`}>
            Bookmark Novels
          </a>
        </span>
        <Link to={{pathname: gatekeeper.sitemap.signin}}>
          <span className='fa fa-sign-in' />
            &nbsp;
            Sign In
          </Link>
        <Link to={{pathname: gatekeeper.sitemap.register}}>
          <span className='fa fa-user-plus' />
            &nbsp;
            Create Account
          </Link>
      </nav>
    )
  }
}
