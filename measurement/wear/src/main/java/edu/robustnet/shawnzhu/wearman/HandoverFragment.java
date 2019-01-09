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

public class HandoverFragment extends Fragment {

    public EditText ipText;
    public Button startBtn;
    public RTClient rtClient;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState){
        View view = inflater.inflate(R.layout.handover_fragment, container, false);

        startBtn = view.findViewById(R.id.start_button);
        ipText = view.findViewById(R.id.ip_text);
        ipText.setText("141.212.110.129");

        startBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                String ipStrValue = ipText.getText().toString();
                Log.d("Shawn", "IP: " + ipStrValue);

                rtClient = new RTClient();
                rtClient.communicate(ipStrValue, getActivity());

            }
        });

        return view;
    }

}
