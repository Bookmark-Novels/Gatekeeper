import React from 'react'
import Helmet from 'react-helmet'

export class PageNotFound extends React.Component {
  render () {
    return (
      <div>
        <Helmet title="Oops. This page doesn't exist" />
        <aside id='gatekeeper-modal'>
          <p>
            This page doesn't exist. <a href={`${gatekeeper.bookmark_host}`}>Go back to Bookmark.</a>
          </p>
        </aside>
      </div>
    )
  }
}
