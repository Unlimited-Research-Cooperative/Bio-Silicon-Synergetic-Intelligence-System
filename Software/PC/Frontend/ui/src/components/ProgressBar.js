import React from "react";
import styles from "../App.module.css";


export default function ProgressBar(prop){
    return (
        <div className={styles.fit_div}>
        <progress className={styles.progress_bar} 
            value={prop.value} max={prop.max} id={prop.id} >
        </progress>
        <p id={prop.id_text} className={styles.text}>{prop.value}%</p>
        </div>
    )
}
