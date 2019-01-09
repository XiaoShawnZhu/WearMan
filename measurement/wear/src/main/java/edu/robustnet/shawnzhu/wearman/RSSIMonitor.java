package edu.robustnet.shawnzhu.wearman;

import android.app.IntentService;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.os.AsyncTask;
import android.os.SystemClock;
import android.util.Log;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Set;
import java.util.concurrent.TimeUnit;


public class RSSIMonitor extends IntentService {

    private static final String TAG = "RSSIMonitor";
    private static final long LOG_TIME = TimeUnit.MINUTES.toMillis(5);
    private static final long LOG_INTERVAL_MILLIS = 200;
    public BluetoothAdapter mBluetoothAdapter;
    public BluetoothManager mBluetoothManager;
    private BluetoothGatt mBluetoothGatt;
    long startTime;
    private int relativeRSSI = 0;
    ConnectivityManager mConnectivityManager;

    @Override
    protected void onHandleIntent(Intent arg0) {
        Log.i(TAG, "Intent Service started on RSSIReader");
    }

    public RSSIMonitor() {
        super("MyIntentService");
        startTime = System.currentTimeMillis();
        new RSSIMonitor.BTTask().execute();
    }

    private class BTTask extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {

            mConnectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
            mBluetoothManager = (BluetoothManager) getSystemService(BLUETOOTH_SERVICE);
            mBluetoothAdapter = mBluetoothManager.getAdapter();

            Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
            String deviceName;
            String deviceHardwareAddress;
            if (pairedDevices.size() > 0) {
                for (BluetoothDevice device : pairedDevices) {
                    deviceName = device.getName();
                    deviceHardwareAddress = device.getAddress(); // MAC address
                    Log.d(TAG, "WearMan "+String.format("+%s+%s", deviceName, deviceHardwareAddress));
                    connectDevice(device);
                    boolean r;
                    try{
                        PrintWriter printWriter = new PrintWriter(new FileWriter("/sdcard/rssi"+System.currentTimeMillis()+".log"));
                        while(System.currentTimeMillis() - startTime < LOG_TIME){
                            r= mBluetoothGatt.readRemoteRssi();
                            printWriter.println(System.currentTimeMillis() + "\t" + relativeRSSI);
                            Log.d(TAG, "Boolean value: "+r);
                            SystemClock.sleep(LOG_INTERVAL_MILLIS);
                        }
                        printWriter.close();
                    }
                    catch(Exception e){

                    }
                }
            }
            return null;
        }
    }
    // Gatt connection
    private void connectDevice(BluetoothDevice device) {
        Log.d(TAG, "Connecting to " + device.getAddress());
        GattClientCallback gattClientCallback = new GattClientCallback();
        mBluetoothGatt = device.connectGatt(this, false, gattClientCallback);
    }

    // Callbacks
    private class GattClientCallback extends BluetoothGattCallback {

        @Override
        public void onReadRemoteRssi(BluetoothGatt gatt, int rssi, int status) {
            super.onReadRemoteRssi(gatt, rssi, status);

            if (status == BluetoothGatt.GATT_SUCCESS) {
                relativeRSSI = rssi;
                Log.d(TAG, System.currentTimeMillis() + " RSSI-relative: " + relativeRSSI);

            } else {
                Log.d(TAG, "RSSI not read successfully.");
            }
        }
    }

}
