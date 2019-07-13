package ca.gcastle.bottomnavigation.view;

import android.content.Context;
import android.util.TypedValue;

/**
 * Created by graeme.castle on 21/04/2016.
 */
public class BottomNavigationUtils {
    public static int getPixelsFromDP(Context context, int dp) {
        return (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, context.getResources().getDisplayMetrics());
    }
}
