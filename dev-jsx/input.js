import React from 'react';

export class Input extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            label: props.label,
            type: props.type,
            value: props.value,
            name: props.name,
            id: props.id,
            placeholder: props.placeholder
        };
    }

    render(){
        return (
            <span className="gatekeeper-form-input-group">
                <label>{this.state.label}</label>
                <input type={this.state.type} value={this.state.value} name={this.state.name} id={this.state.id} placeholder={this.state.placeholder} required />
            </span>
        );
    }
}
