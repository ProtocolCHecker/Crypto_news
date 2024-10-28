
import requests
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import streamlit as st


def fetch_merge_news(headers, params, source_name):
    url = 'https://x.com/i/api/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets'
    
    # Make the request
    response = requests.get(url, headers=headers, params=params)

    # Recursive function to find both "created_at" and corresponding "full_text"
    def find_date_text_pairs(json_data):
        results = []
        if isinstance(json_data, dict):
            created_at = json_data.get('created_at')
            full_text = json_data.get('full_text')
            if created_at and full_text:
                results.append((created_at, full_text))
            for key, value in json_data.items():
                results.extend(find_date_text_pairs(value))
        elif isinstance(json_data, list):
            for item in json_data:
                results.extend(find_date_text_pairs(item))
        return results

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        date_text_pairs = find_date_text_pairs(data)

        # Group texts by hour, using a set to remove duplicates
        grouped_texts = defaultdict(set)
        for date_str, text in date_text_pairs:
            date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
            group_key = date_obj.replace(minute=0, second=0)
            grouped_texts[group_key].add(text)

        # Concatenate unique texts within the same hour
        concatenated_results = [(source_name, key.strftime('%Y-%m-%d %H:%M:%S'), ' '.join(texts)) for key, texts in grouped_texts.items()]
        df_concatenated = pd.DataFrame(concatenated_results, columns=["News Paper", 'Created At', 'Concatenated Text'])
        return df_concatenated
    else:
        st.write(f"Failed to fetch data for {source_name}. Status code: {response.status_code}")
        return pd.DataFrame(columns=["News Paper", 'Created At', 'Concatenated Text'])  # Return empty DataFrame on failure


def fetch_and_sort_news():
    cURL_sources = {
        "defiant": {
            "headers": {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/DefiantNews',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'mpiRUm5iSztwyDezN2YZg7GA6vANgF5g39+I7a+0JGWZdzmFJTFoPqeICpjcAe9IUR6sVpiM6Quu4wd0WvW0Xohnp8HAmQ',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params": {
                "variables": '{"userId":"1237544865216507906","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "blockworks": {
            "headers": {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/Blockworks_',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'TYo7zIN3Q6WcFO8WN6qmLobCvGMi5103ti5I0K6dvWnK19WZs1POUnbgO2AEKD0KzXJ6gU8T6gvVAYfmkIaU1DFOXk3xTg',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params": {
                "variables": '{"userId":"989912836901089282","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "cointelegraph": {
            "headers": {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/Cointelegraph',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'yc8+i5v0NuvIxKE7MK21mVD09p05RtlRVedYBk8JbJ6c0fYvafHjnuc4y+NLd8LKA8bxBcvGPaMx7aTvPrp3t3t+Fg8kyg',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params": {
                "variables": '{"userId":"2207129125","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "beincrypto": {
            "headers": {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/beincrypto',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'gJgMjCKLTd5JhrhGg10fgB5BHK6yj12oG8y+pZ576asDi/u05Eic58JNA3igOBK6j7BZTIKjU8K0CH3KpxRIHeezB6hhgw',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params" : {
                "variables": '{"userId":"1021643080208801792","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "cryptoslate":{
            "headers" : {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/CryptoSlate',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'bi5i1riZR9dojnZMyTSLwpFeKJ4U1IztrWex5MEumF0U3vzrtwqqjQToeYOFQIsZOoS1omzZ3fMM9KtOeFwck0qOWe+bbQ',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
                },
            "params" : {
                "variables": '{"userId":"893284234042855424","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "watcher guru": {
            "headers" : {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/WatcherGuru',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'xXkWoh2dM3qo5okaheqAH3nNK5dxpBb3ZQMXRzGfoaHMsJzaxcQJf54Fb5O3ok78wQ8ZCcd4z8Im1IUeLtTBaGYn+42vxg',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params" : {
                "variables": '{"userId":"1387497871751196672","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "intotheblock": {
            "headers" : {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/intotheblock',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'eUGutPNV2vo3sfzV8iHU9RisVuB0Z3gxXVeWBPYONGE+uhZxFeBUYovUtmmXbrBhvzCntXtbg10Up78ydwbHONWOqqyieg',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params" : {
                "variables": '{"userId":"1095652151903297536","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        },
        "coindesk": {
            "headers" : {
                'accept': '*/*',
                'accept-language': 'en-GB,en;q=0.7',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'content-type': 'application/json',
                'cookie': 'd_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; night_mode=2; kdt=pwpwZYSzwDBacJpvMx4yZ68YNGgQdXe3kf70nkLD; lang=en; dnt=1; ads_prefs="HBISAAA="; auth_multi="1685099351264104450:bb29ca59ac46232e8ec69769a105ff26d1a2b258"; auth_token=4a074df2e15fb872da8efac12114fe632e8f42ea; guest_id=v1%3A172650648856670354; twid=u%3D1273212852418027522; ct0=6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff; guest_id_marketing=v1%3A172650648856670354; guest_id_ads=v1%3A172650648856670354; external_referer=padhuUp37zhzf%2BzW9lbDSEb6StpkXI7fDirGjZNZuxk%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_A6IpAVzskxFxet2WTYrhNA=="',
                'priority': 'u=1, i',
                'referer': 'https://x.com/CoinDesk',
                'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-client-transaction-id': 'yHjaTRmQx77eW81z5HIUKkwFzTxjORU6dUVW8ts6qgvQmdgQ9Igd2suR46tcy8asNq0XBMp+eUdWvgHEnNN5Q9oC6+mKyw',
                'x-client-uuid': 'df624196-4adb-45bb-aa12-74abafdd165b',
                'x-csrf-token': '6fe4c1ef6b4e1168cd3f2ac393f816cb1e68f6121fa80a486a4112baeee145ad47faa0977f482b76810a41719ff7afe29f3e8824aec6677533823c4cdfe4addc60ebb9eba8599b9fd6b526aabf6187ff',
                'x-twitter-active-user': 'no',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            },
            "params" : {
                "variables": '{"userId":"1333467482","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
                "features": '{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
                "fieldToggles": '{"withArticlePlainText":false}'
            }
        }
    }

    # Fetch and merge news for all sources
    all_news_df = pd.DataFrame(columns=["News Paper", 'Created At', 'Concatenated Text'])
    for source_name, config in cURL_sources.items():
        headers = config["headers"]
        params = config["params"]
        news_df = fetch_merge_news(headers, params, source_name.capitalize())
        all_news_df = pd.concat([all_news_df, news_df], ignore_index=True)

    # Convert 'Created At' to datetime format and sort by it in descending order
    all_news_df['Created At'] = pd.to_datetime(all_news_df['Created At'])
    all_news_df = all_news_df.sort_values(by='Created At', ascending=False).reset_index(drop=True)

    return all_news_df


def filter_news_by_protocols(news_df, protocols):
    # Convert protocols to lowercase for case-insensitive matching
    protocols_lower = [protocol.lower() for protocol in protocols]
    
    # Find matching protocols in 'Concatenated Text' and add a 'Matched Protocols' column
    matched_protocols = []
    for text in news_df['Concatenated Text'].str.lower():
        matched = [protocol for protocol in protocols_lower if protocol in text]
        matched_protocols.append(", ".join(matched).title())  # Format matched protocols in title case

    # Add 'Matched Protocols' column to news_df and filter only rows where at least one protocol was matched
    news_df['Matched Protocols'] = matched_protocols
    filtered_df = news_df[news_df['Matched Protocols'] != ""]

    # Reorder columns to place 'Matched Protocols' between 'News Paper' and 'Created At'
    filtered_df = filtered_df[['News Paper', 'Matched Protocols', 'Created At', 'Concatenated Text']]
    
    return filtered_df

# List of protocols and associated tokens
protocols = [
    "Uniswap", "GMX", "Aave", "Synthetix", "THORChain", "Rocket Pool", "Lido", 
    "Frax", "Akash", "Near", "The Graph", "Avalanche", "Arbitrum", "Optimism", 
    "Ethereum", "Solana", "Render", "API3"
]

# def filter_news_by_protocols(news_df, protocols_tokens):
#     # Create a combined list of protocols and tokens for case-insensitive matching
#     protocols_tokens_lower = {protocol.lower(): [token.lower() for token in tokens] for protocol, tokens in protocols_tokens.items()}
    
#     # Find matching protocols and tokens in 'Concatenated Text' and add a 'Matched Protocols' column
#     matched_protocols = []
#     for text in news_df['Concatenated Text'].str.lower():
#         matched = []
#         for protocol, tokens in protocols_tokens_lower.items():
#             # Check if protocol name or any associated token is in the text
#             if protocol in text or any(token in text for token in tokens):
#                 matched.append(protocol.title())  # Add protocol in title case for display
#         matched_protocols.append(", ".join(matched))

#     # Add 'Matched Protocols' column to news_df and filter only rows where at least one protocol was matched
#     news_df['Matched Protocols'] = matched_protocols
#     filtered_df = news_df[news_df['Matched Protocols'] != ""]

#     # Reorder columns to place 'Matched Protocols' between 'News Paper' and 'Created At'
#     filtered_df = filtered_df[['News Paper', 'Matched Protocols', 'Created At', 'Concatenated Text']]
    
#     return filtered_df


# # Dictionary of protocols and their associated tokens
# protocols_tokens = {
#     "Uniswap": ["UNI"],
#     "GMX": ["GMX"],
#     "Aave": ["AAVE"],
#     "Synthetix": ["SNX"],
#     "THORChain": ["RUNE"],
#     "Rocket Pool": ["RPL"],
#     "Lido": ["LDO"],
#     "Frax": ["FRAX"],
#     "Akash": ["AKT"],
#     "Near": ["NEAR"],
#     "The Graph": ["GRT"],
#     "Avalanche": ["AVAX"],
#     "Arbitrum": ["ARB"],
#     "Optimism": ["OP"],
#     "Ethereum": ["ETH"],
#     "Solana": ["SOL"],
#     "Render": ["RNDR"],
#     "API3": ["API3"]
# }


# Streamlit app
st.title("Crypto News Aggregator")

if st.button("Fetch and Display Latest News"):
    # Run the function when the button is pressed
    news_df = fetch_and_sort_news()
    
    # Display the full table of news
    if not news_df.empty:
        st.write("### All News Ordered by Date")
        st.dataframe(news_df)
        
        # Filter and display only relevant protocol news
        protocol_news_df = filter_news_by_protocols(news_df, protocols)
        st.write("### News Related to Specific Protocols")
        st.dataframe(protocol_news_df)
    else:
        st.write("No data available or failed to fetch news.")

