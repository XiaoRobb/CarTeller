package com.shashank.platform.loginui;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.IOException;

import handler.HttpHandler;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class RegisterActivity extends AppCompatActivity {

    Button submit;
    EditText uname;
    EditText pwd;
    ImageView imageView;
    TextView textView;
    String URL = LoginActivity.URL;

    private Handler handler= new Handler(){
        //处理服务器返回的json
        public void handleMessage(Message msg){
            if(msg.what == 2) {
                try {
                    JSONObject obj = new JSONObject(msg.obj.toString());
                    String returnName = obj.getString("username");
                    if (returnName.equals("-1")) {
                        onSuccess(false);
                    } else {
                        onSuccess(true);
                    }
                } catch (Exception e) {
                    Log.d("handler", "handleMessage: "+e.toString());
                }
            }
        }
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_register);
        imageView = findViewById(R.id.imageView2);
        textView = findViewById(R.id.textView);
        setContentView(R.layout.activity_register);
        submit = findViewById(R.id.submit);
        uname = findViewById(R.id.rusername);
        pwd = findViewById(R.id.rpassword);

        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String myname = uname.getText().toString();
                String mypwd = pwd.getText().toString();
                if (myname != null && mypwd != null) {
                    registerRequest(RegisterActivity.this, uname.getText().toString(), pwd.getText().toString());
                } else {
                    Toast.makeText(RegisterActivity.this, "用户名和密码都不能为空！", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
    public void onSuccess(Boolean succ){
        if(succ){
            final AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("提示").setMessage("注册成功！").setPositiveButton("确定", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    //确定按钮的点击事件
                    Intent it = new Intent(RegisterActivity.this, LoginActivity.class);
                    startActivity(it);
                }
            }).show();
        }else {
            Toast.makeText(RegisterActivity.this,"注册失败，请使用其他用户名！",Toast.LENGTH_SHORT).show();
        }
    }
    public void onFailure(){
        Toast.makeText(RegisterActivity.this,"注册失败，请检查网络后重试",Toast.LENGTH_SHORT).show();
   }


    //注册处理函数
    public void registerRequest(final RegisterActivity register, String name, String pwd) {
        FormBody formBody = new FormBody.Builder()
                .add("username", name)
                .add("password", pwd)
                .build();
        //请求组合创建
        final Request request = new Request.Builder()
                .url(URL + "/register")
                .post(formBody)
                .build();
        //发起请求
        OkHttpClient mOkHttpClient = new OkHttpClient();
        mOkHttpClient.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                //请求失败时
                register.onFailure();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                //请求返回时,返回json，进行判断
                try {
                    String json = response.body().string();
                    handler.obtainMessage(2,json).sendToTarget();

                } catch (Exception e) {
                    Log.d("onsucc", e.toString());
                }
            }
        });
    }
}
