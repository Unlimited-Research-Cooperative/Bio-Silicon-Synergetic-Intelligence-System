import React from 'react'
import styles from "../App.module.css";

function LogBar(props) {
    let color = "";
    if (props.type == "INFO") {
        color = "#3A86B7"
    }
    if (props.type == "ERROR") {
        color = "red";
    }

    if (props.type == "WARN") {
        color = "yellow";
    }

    return (
        <div className={styles.log_bar}
            style={
                {
                    border: '1px solid '.concat(color),
                    boxShadow: 'inset 0 0 10px '.concat(color),
                    marginTop: '10px'
                }
            }
            id={props.id}
        >
            <p id={'log_type'} style={{ fontWeight: 'bold' }} >{props.type}</p>
            <p id={'msg'} style={{ flex: 1, textAlign: 'center' }} >{props.message}</p>
            <p id={'time'}>{props.time}</p>
        </div>
    )
}

export default LogBar
