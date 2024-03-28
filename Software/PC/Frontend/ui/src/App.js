import styles from "./App.module.css";
import callPrint from "./webchannel/channel";
import ProgressBar from "./components/ProgressBar";
import StressMeter from "./components/StressMeter";

export default function Home() {
  return (
    <main className={styles.main_window}>
      <div style={{display: 'flex', flexDirection: 'column'}}>
        <h3>Buttons</h3>
        <div style={{display: 'flex', gap: '20px'}}>
          <button className={styles.button_normal} onClick={callPrint}>Normal Button</button>
          <button className={styles.button_danger}>Danger Button</button>
          
        </div>
        <p>Simple Text With Nice Font</p>
        <h3>A Nice Progress Bar</h3>
        <ProgressBar value={15} max={50} id_text={"progress-text"} id={"progress-bar"} />
        <h3>The Stress Meter</h3>
        <StressMeter />
        <h3>A Text Box</h3>
        <input className={styles.text_input} placeholder="Placeholder" />
      </div>
    </main>
  );
}
