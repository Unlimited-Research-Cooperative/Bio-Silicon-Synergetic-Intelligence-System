import React from "react";
import styles from "../page.module.css";

function increaseVal(id_bar, id_text){
    var progressBar = document.getElementById(id);
    var progressText = document.getElementById(id_text);
    var width = parseInt(progressBar.style.width, 10);
    width = Math.min(width + 10, 100); // Increase progress and clamp at 100%
    progressBar.style.width = width + '%'; 
    progressText.textContent = width + '%'; // Update text
}

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
