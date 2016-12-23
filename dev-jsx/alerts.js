import React from 'react';

export class Alert extends React.Component {
    render(){
        return (
            <div className={ 'alert ' + this.props.type }>
                { this.props.children }
            </div>
        );
    }
}

export class Alerts extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
            <aside className="alerts">
                { this.props.children }
            </aside>
        );
    }
}
