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

public class BasicFragment extends Fragment {

    private static final String TAG = "BasicFragment";
    private RadioGroup radioDirGroup;
    public EditText sizeText;
    public EditText ipText;
    public Button startBtn;
    public TCPClient tcpClient;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
        View view = inflater.inflate(R.layout.basic_fragment, container, false);

        radioDirGroup = view.findViewById(R.id.direction);
        sizeText = view.findViewById(R.id.size_text);
        sizeText.setText("3000");
        ipText = view.findViewById(R.id.ip_text);
        ipText.setText("141.212.110.129");
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

                String sizeStrValue = sizeText.getText().toString();
                String ipStrValue = ipText.getText().toString();
                Log.d(TAG, "Direction: " + ((direction==1)?"UP":"DOWN") +
                        ", size in KB: " + sizeStrValue + ", IP: " + ipStrValue);

                tcpClient = new TCPClient();
                tcpClient.communicate(direction, 1000*Integer.parseInt(sizeStrValue), 0, ipStrValue);

            }
        });

        return view;
    }

}
