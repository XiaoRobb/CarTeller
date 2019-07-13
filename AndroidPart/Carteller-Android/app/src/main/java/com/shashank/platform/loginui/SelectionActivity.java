package com.shashank.platform.loginui;

import android.content.Intent;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.view.ViewPager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TableLayout;

import java.util.ArrayList;
import java.util.List;

import ca.gcastle.bottomnavigation.listeners.OnChildClickedListener;
import ca.gcastle.bottomnavigation.view.BottomNavigationView;

public class SelectionActivity extends AppCompatActivity {

    private BottomNavigationView bottomNavigationView;
    private ViewPager viewPager;

    private boolean clickTransition;
    public String session;
    public static String username;
    List<String> titles;
    List<Fragment> fragments;
    Button uinfoBtn, recoBtn;

    Fragment recoF=null;
    Fragment uinfoF=null;

    FragmentTransaction ftr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        //获取验证码，也可获取用户名和密码，做个个人信息界面，不过不重要
        setContentView(R.layout.activity_selection);


        //对字段数据进行初始化
        Intent it = getIntent();
        session = it.getStringExtra("session");
        username = it.getStringExtra("username");
        titles = new ArrayList<String>();
        titles.add("车辆识别");
        titles.add("个人信息");
        fragments = new ArrayList<Fragment>();

        fragments.add(new RecognizeFragment());
        fragments.add(new UserinfoFragment());

        //绑定组件
        setupBottomNavigationView();
        setupViewPager();

    }

    public void setupBottomNavigationView() {
        bottomNavigationView = (BottomNavigationView) findViewById(R.id.bottom_navigation);
        //点击Tab时
        bottomNavigationView.setOnChildClickedListener(new OnChildClickedListener() {
            @Override
            public void onChildClicked(int child) {
                clickTransition = true;
                viewPager.setCurrentItem(child);
                clickTransition = false;
            }
        });

    }

    public void setupViewPager() {
        String[] fragmentTitles = new String[] {
                "车辆识别",
                "个人信息"
        };

        RecognizeFragmenAdapter adapter = new RecognizeFragmenAdapter(getSupportFragmentManager(), fragmentTitles);
        viewPager = (ViewPager) findViewById(R.id.viewPager);
        viewPager.setAdapter(adapter);
    }


    //隐藏fragment
    private void hideTransaction(FragmentTransaction ftr) {

        if (recoF != null) {
            ftr.hide(recoF);//隐藏该fragment
        }
        if (uinfoF != null) {
            ftr.hide(uinfoF);
        }
    }
}
