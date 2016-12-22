import React from 'react';

export class Input extends React.Component {
    render(){
        let input = React.createElement('input', this.props);

        return (
            <span className="gatekeeper-form-input-group">
                <label>{this.props.label}</label>
                { input }
            </span>
        );
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
 * contents is restored.
 *
 * Additionally, you may manually invoke the enable/disable
 * functionality by calling `WorkButton#enable` and `WorkButton#disable`.
 */
export class WorkButton extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            working: false
        };
    }

    enable(){
        this.props.disabled = true;
        this.setState({
            working: true
        });
    }

    disable(){
        this.props.disabled = false;
        this.setState({
            working: false
        });
    }

    handleClick(){
        disable();

        if(this.props.job){
            this.props.job(this._doneWorking);
        }
    }

    _doneWorking(){
        enable();
    }

    render(){
        let contents = this.props.children;

        if(this.state.working){
            contents = <span className="fa fa-spin fa-circle-o-notch" />;
        }

        return React.createElement('button', this.props, contents);
    }
}
