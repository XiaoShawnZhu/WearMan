package edu.robustnet.shawnzhu.wearman;

import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.IBinder;
import android.util.Log;

public class RSSIReader extends Service {

    private static final String TAG = "RSSIReader";

    private BluetoothAdapter BTAdapter = BluetoothAdapter.getDefaultAdapter();
    BluetoothBroadcastReceiver receiver = null;

    @Override
    public void onCreate() {

        receiver = new BluetoothBroadcastReceiver();
        registerReceiver(receiver, new IntentFilter(BluetoothDevice.ACTION_FOUND));
        BTAdapter.startDiscovery();
    }

    @Override
    public IBinder onBind(Intent intent) {
        // A client is binding to the service with bindService()
        return null;
    }

    private class BluetoothBroadcastReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                int rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI, Short.MIN_VALUE);
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                String name = device.getAddress().toLowerCase();
                if ("40:4e:36:d9:ec:cf".equals(name)) {
                    Log.d(TAG, "Paired device: " + name + " => " + rssi + "dBm");
                    BTAdapter.cancelDiscovery();
                }
                Log.v(TAG, "bluetooth: " + name + " => " + rssi + "dBm");
            }
        }
    }

}