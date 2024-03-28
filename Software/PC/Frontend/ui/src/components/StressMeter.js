import React from "react";
import styles from "../App.module.css";

export default function StressMeter(){
    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            <progress className={styles.stress_meter} value={15} max={100} 
            style={{height: '150px', width: '30px'}} />
            <p>LOW</p>
        </div>
    )
}
