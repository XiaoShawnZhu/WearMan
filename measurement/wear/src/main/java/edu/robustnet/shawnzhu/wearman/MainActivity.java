package edu.robustnet.shawnzhu.wearman;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.support.wear.ambient.AmbientModeSupport;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

public class MainActivity extends AppCompatActivity implements AmbientModeSupport.AmbientCallbackProvider {

    private Spinner spinner;

    private BasicFragment basicFragment;
    private HandoverFragment handoverFragment;
    private CBRFragment cbrFragment;

    private AmbientModeSupport.AmbientController mAmbientController;

    @Override
    public AmbientModeSupport.AmbientCallback getAmbientCallback() {
        return new MyAmbientCallback();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Enables Always-on
        mAmbientController = AmbientModeSupport.attach(this);

        basicFragment = new BasicFragment();
        handoverFragment = new HandoverFragment();
        cbrFragment = new CBRFragment();

        spinner = findViewById(R.id.type_spinner);

        ArrayAdapter<String> adapter = new ArrayAdapter<>(MainActivity.this,
                R.layout.custom_spinner,
                getResources().getStringArray(R.array.type_arrays));
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);

        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

                switch (position) {
                    case 0:
                        Log.d("Shawn", "basic selected");
                        setFragment(basicFragment);
                        break;
                    case 1:
                        Log.d("Shawn", "cbr selected");
                        setFragment(cbrFragment);
                        break;
                    case 2:
                        Log.d("Shawn", "handover selected");
                        setFragment(handoverFragment);
                        break;

                }

            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

                // sometimes you need nothing here
            }

        });

    }

    private class MyAmbientCallback extends AmbientModeSupport.AmbientCallback {
        @Override
        public void onEnterAmbient(Bundle ambientDetails) {
            // Handle entering ambient mode
        }

        @Override
        public void onExitAmbient() {
            // Handle exiting ambient mode
        }

        @Override
        public void onUpdateAmbient() {
            // Update the content
        }
    }

    public void setFragment(Fragment fragment){
        FragmentTransaction fragmentTransaction = getSupportFragmentManager().beginTransaction();
        fragmentTransaction.replace(R.id.main_frame, fragment);
        fragmentTransaction.commitAllowingStateLoss();
    }


}
