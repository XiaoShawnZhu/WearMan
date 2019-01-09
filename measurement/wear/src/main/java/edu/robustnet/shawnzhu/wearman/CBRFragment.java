package edu.robustnet.shawnzhu.wearman;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioGroup;

public class CBRFragment extends Fragment {

    private static final String TAG = "CBRFragment";
    private RadioGroup radioDirGroup;
    public EditText durationText;
    public EditText ipText;
    public EditText rateText;
    public Button startBtn;
    public TCPClient tcpClient;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
        View view = inflater.inflate(R.layout.cbr_fragment, container, false);

        radioDirGroup = view.findViewById(R.id.direction);
        durationText = view.findViewById(R.id.duration_text);
        durationText.setText("10");
        ipText = view.findViewById(R.id.ip_text);
        ipText.setText("141.212.110.129");
        rateText = view.findViewById(R.id.rate_text);
        rateText.setText("100");
        startBtn = view.findViewById(R.id.start_button);

        startBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                int direction = 0;

                // get selected radio button from radioGroup
                int selectedId = radioDirGroup.getCheckedRadioButtonId();

                // Check which radio button was clicked
                if(selectedId == R.id.upload_button) {
                    Log.d(TAG, "up");
                    direction = 0;
                }
                else if(selectedId == R.id.download_button) {
                    Log.d(TAG, "down");
                    direction = 1;
                }

                String durStrValue = durationText.getText().toString();
                String ipStrValue = ipText.getText().toString();
                String rateStrValue = rateText.getText().toString();
                Log.d(TAG, "Direction: " + ((direction==1)?"UP":"DOWN") +
                        ", duration in sec: " + durStrValue + ", kbps: " + rateStrValue + ", IP: " + ipStrValue);

                tcpClient = new TCPClient();
                tcpClient.communicate(direction,1000*Integer.parseInt(durStrValue)*Integer.parseInt(rateStrValue)/8,
                        1000*Integer.parseInt(rateStrValue), ipStrValue);

            }
        });

        return view;
    }

}
