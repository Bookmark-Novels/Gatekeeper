import React from 'react'

export class NavBar extends React.Component {
  render () {
    return (
      <nav>
        <span id='bookmark-logo'>
          <a href={`${gatekeeper.bookmark_host}`}>
            <span className='full-width'>
              Bookmark Novels
            </span>
            <span className='small-width'>
              BN
            </span>
          </a>
        </span>
        <a href={`${gatekeeper.sitemap.signin}`}>
          <span className='fa fa-sign-in' />
            &nbsp;
            Sign In
          </a>
        <a href={`${gatekeeper.sitemap.register}`}>
          <span className='fa fa-user-plus' />
            &nbsp;
            Create Account
          </a>
      </nav>
    )
  }
}
