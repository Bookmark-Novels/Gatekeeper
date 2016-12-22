import React from 'react';

export class Alert extends React.Component {
    render(){
        return (
            <div className={ 'alert ' + this.props.type }>
                { this.children }
            </div>
        );
    }
}

export class Alerts extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            alerts: this.props.children
        };
    }

    alert(alert){
        let alerts = this.state.alerts;
        alerts.push(alert);

        this.setState({
            alerts: prev.alerts
        });
    }

    render(){
        return (
            <aside className="alerts">
                { this.state.alerts }
            </aside>
        );
    }
}
