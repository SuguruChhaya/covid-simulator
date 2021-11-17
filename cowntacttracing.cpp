#include <bits/stdc++.h>
using namespace std;

int main(){

    freopen("tracing.in", "r", stdin);
    freopen("tracing.out", "w", stdout);

    long long n, t;
    cin >> n >> t;
    string s;
    cin >> s;

    //!Identifying the infected cow. 
    vector <long long> infected;
    for (long long i=1;i<=n;i++){
        if (s[i-1]=='1'){
            //*I will 1-index this too. 
            infected.push_back(i);
        }
    }
    
    
    vector <vector <long long>> arr;
    for (long long i=0;i<t;i++){
        long long t, x, y;
        cin >> t >> x >> y;
        //!So much information to consider here huh??
        arr.push_back({t, x, y});
    }

    sort(arr.begin(), arr.end());   

    set <long long> ok_cows;
    long long x, y, z;
    string infinity;

    //*y could be 0. 
    y = 999999999;
    //*I don't think there is a problem initializing z as 0 too. 
    z = 0;

    //!I don't need to simulate all cows as patient zero since when a cow is infected, it will stay infected. 

    

    for (auto zero:infected){
        //!I think there has to be an upper bound for K to determine whether infinity or not. 
        for (long long k=0;k<=t;k++){
            //*If it applies for all the number of interactions it should be able to continue forever. 
            string currInfected;
            vector <long long> k_arr;
            
            for (long long i=0;i<=n;i++){
                //*1-indexed. 
                k_arr.push_back(0);
            }
            for (long long h=0;h<=n;h++){
                currInfected.push_back('0');
            }
            //*Pretty sure I have to make the zero'th dude infected. 
            currInfected[zero] = '1';
            for (auto shake:arr){
                auto temp_string = currInfected;
                //!Remember that shake[0] is just the time!!
                if (currInfected[shake[1]]=='1' && k_arr[shake[1]]<k){
                    //*Before adding on, I have to check whether it is already at k_value or not. 
                    k_arr[shake[1]]++;
                    //!Has to be simultaneous update so maybe the second cow wasn't infected but now that we put it as infected it gets infected...
                    //*Or I could create a next string and make modifications there. 

                    temp_string[shake[2]] = '1';
                }

                if (currInfected[shake[2]]=='1' && k_arr[shake[2]] < k){
                    //*Second cow is infected. 
                    k_arr[shake[2]]++;
                    temp_string[shake[1]] = '1';
                }

                //*Now assign the correct string. 
                currInfected = temp_string;
            }

            //*After all the shakes compare:
            //!I get it, I 1-indexed but I am comparing length 5 and 4!!
            if (currInfected.substr(1, n)==s){
                //*Add the cow but the same cow might be OK for several different K values so add in a set. 
                ok_cows.insert(zero);
                //*Check whether this makes the min value or the max value. 
                y = min(y, k);
                z = max(z, k);


            }
        }

        if (z == t){
            z = -1;
        }
        
        //*If z ended up being t (so all interactions give correct answer), then change it to -1 (for identification) and set a string for the answer. 
    }
    x = ok_cows.size();

    cout << x << " " << y << " ";
    if (z==-1){
        cout << "Infinity" << endl;
    }
    else{
        cout << z << endl;
    }

    //!I am getting an all 0 lol. 
    
}