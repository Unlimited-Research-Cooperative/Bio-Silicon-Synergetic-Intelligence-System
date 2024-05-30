The actual signals are captured throug MEA implanted in the subject's brain. But for testing software, we use simulated signals. This Signal Simulator tool generates signals and publishes them over the same topic as that of actual data. These signals are then received by the ==data manager== instances subscribed to the topic.

!!! note
    Please refer to Topics section in System Design to see active topics.

![text](https://raw.githubusercontent.com/Raghav67816/Bio-Silicon-Synergetic-Intelligence-System/main/images/Signal%20Simulator%20UI.png)

The UI is simple but it has a lot of parameter to input by the user. To make this process more simpler you have to input the values once, then you `Save` & `Load` your configurations.


### Progress
 - [x] Basic user interface
 - [x] Error handling
 - [x] Publish Messages
 - [x] Save & Get values
 - [x] Stable Release

### Parameters & Discription

| Key                 | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `min_volt`          | 1 microvolt                                                                 |
| `max_volt`          | 8 microvolts                                                                |
| `variability_factor`| Direct mapping of player movement to variability factor, normalized to 0-1  |
| `variance`          | Mapping door state to variance feature                                      |
| `std_dev`           | Mapping enemy type to standard deviation feature                            |
| `rms_value`         | Player health state affects the RMS value feature                           |
| `num_peaks`         | Number of peaks determined by exploring states                              |
| `peak_height`       | Peak height influenced by level state                                       |
| `fractal_dimension` | Action states influence the fractal dimension                               |
| `window_size`       | Window size feature influenced by wall states                               |
| `target_rate`       | Target rate is determined by the presence of any enemy type                 |
| `min_freq`          | Minimum frequency affected by player movement                               |
| `max_freq`          | Maximum frequency influenced by player health state                         |
| `blend_factor`      | Static blend factor as a static state                                       |
| `global_sync_level` | Global sync level determined by action state                                |
| `pairwise_sync_level`| Pairwise sync level affected by door state                                 |
| `sync_factor`       | Sync factor as a static value for simplicity                                |
| `influence_factor`  | Influence factor derived from enemy type                                    |
| `max_influence`     | Maximum influence as a static maximum for the presence of any enemy         |
| `centroid_factor`   | Centroid factor and edge density factor as placeholders for sensory data encoding |
| `edge_density_factor`| Centroid factor and edge density factor as placeholders for sensory data encoding |
| `complexity_factor` | Example value for complexity factor in FFT                                  |
| `evolution_rate`    | Evolution rate as a static value for dynamic environmental changes          |
| `low_freq`          | Low frequency ranges influenced by exploring states                         |
| `high_freq`         | High frequency ranges influenced by level states                            |
| `causality_strength`| Causality strength as a static value for interaction effects                |
| `num_imfs`          | Number of intrinsic mode functions (IMFs) as a static value for interaction effects |


A dialog will open up asking for some more parameters. These parameters define signals.

![text](https://raw.githubusercontent.com/Raghav67816/Bio-Silicon-Synergetic-Intelligence-System/main/images/Signal%20Simulator%20UI.png)


| Key                 | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `num_signals`       | Number of signals you want to generate                                                              |
| `bit_depth`          |                                                                 |
| `duration`          |                                                                 |
| `sampling_frequency`          | |

After you provide all the inputs, it will generate the signals and send **transformed signals** to topic **SIGNALS**. Then it will plot these signals and write them to your current directory as image files.

![text](https://raw.githubusercontent.com/Unlimited-Research-Cooperative/Human-Brain-Rat/main/images/biomimetic_signals.png)