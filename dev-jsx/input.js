import React from 'react';

export class Input extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        var input = React.createElement('input', this.props);

        return (
            <span className="gatekeeper-form-input-group">
                <label>{this.props.label}</label>
                { input }
            </span>
        );
    }
}
