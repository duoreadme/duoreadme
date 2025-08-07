## Apply Secrets

### Tencent secrets

TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY / secret_id / secret_key

Apply in [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi), select `新建密钥`。

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-08-08-00-03-43.png)

### DuoReadme BOT secrets / bot_app_key

In your [application page](https://lke.cloud.tencent.com/lke#/app/home), select `调用` then find it in `appkey`.

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-08-08-00-04-09.png)

### GH_TOKEN

You can apply GH_TOKEN in `Settings` - `Developer settings` - `Personal access tokens` - `Tokens(classic)` - `Generate new token` - `No expiration` - `Selection: repo and workflow`.

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-08-08-00-04-46.png)


## Add secrets to repo

Add required secrets to your repository `your repository` - `settings` - `Securities and variables` - `Actions` - `New repository secret`.

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-08-08-00-05-30.png)

Then final should be (Must name as the same as the github action):

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-08-08-00-06-14.png)
