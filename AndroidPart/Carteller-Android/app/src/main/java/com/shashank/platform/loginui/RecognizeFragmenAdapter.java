package com.shashank.platform.loginui;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentStatePagerAdapter;

public class RecognizeFragmenAdapter extends FragmentStatePagerAdapter {
    private  String[] titles;
    public RecognizeFragmenAdapter(FragmentManager manager, String[]titles) {
        super(manager);
        this.titles = titles;
    }

    @Override
    public Fragment getItem(int i) {
        if(i == 0) {
            return RecognizeFragment.newInstance(titles[i], i);
        }else{
            return UserinfoFragment.newInstance(titles[i],i);
        }
    }

    @Override
    public int getCount() {
        return titles.length;
    }
}
