import React from 'react'

export class Input extends React.Component {
  value () {
    return this.input.value
  }

  render () {
    return (
      <span className='gatekeeper-form-input-group'>
        <label>{this.props.label}</label>
        <input {...this.props} ref={(c) => { this.input = c }} />
      </span>
    )
  }
}

/**
 * WorkButton represents a button that should be used
 * to execute some possible long-running work.
 *
 * WorkButton takes the property `job` which should be a
 * function that takes a callback function. The callback
 * function should be used to indicate to the WorkButton
 * that the work is done.
 *
 * When a WorkButton is clicked, the button becomes disabled
 * and its contents is replaced with a spinner. When the callback
 * passed to `job` is called, the button becomes enabled and its
 * contents is restored. You can also control the state of the button
 * by passing along a `working` property. The `working` property should
 * be passed within the parent's render method.
 *
 * If no `job` property is specified, this component's state will
 * be determined entirely by the `working` property.'
 *
 * Additionally, you may manually invoke the enable/disable
 * functionality by calling `WorkButton#enable` and `WorkButton#disable`.
 */
export class WorkButton extends React.Component {
  constructor (props) {
    super()
    this.state = {
      working: props.working || false
    }
  }

  enable () {
    this.props.disabled = true
    this.setState({
      working: false
    })
  }

  disable () {
    this.setState({
      working: true
    })
  }

  handleClick () {
    this.disable()

    if (this.props.job) {
      this.props.job(this.enable)
    }
  }

  render () {
    let {working, ...props} = this.props
    let contents = this.props.children

    if ((this.props.job && this.state.working) || this.props.working) {
      contents = <span className='fa fa-spin fa-circle-o-notch' />
    }

    props.onClick = this.handleClick.bind(this)

    return React.createElement('button', props, contents)
  }
}
