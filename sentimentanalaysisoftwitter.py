{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "8238e6c7-535d-4fe8-b445-929b2b73a388",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "#plotting\n",
    "import seaborn as sns\n",
    "from wordcloud import WordCloud\n",
    "import matplotlib.pyplot as plt\n",
    "#nltk\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "#sklearn\n",
    "from sklearn.svm import LinearSVC\n",
    "from sklearn.naive_bayes import BernoulliNB\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.metrics import confusion_matrix,classification_report\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "d20e5f41-b12b-4661-9415-c2e7bed6fd4e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>target</th>\n",
       "      <th>ids</th>\n",
       "      <th>date</th>\n",
       "      <th>flag</th>\n",
       "      <th>user</th>\n",
       "      <th>text</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>10383</th>\n",
       "      <td>0</td>\n",
       "      <td>1550900222</td>\n",
       "      <td>Sat Apr 18 07:35:00 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>amazingphoebe</td>\n",
       "      <td>MY INTERNET IS SOMEWHAT WORKING! I want seb</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>22541</th>\n",
       "      <td>0</td>\n",
       "      <td>1557512136</td>\n",
       "      <td>Sun Apr 19 04:33:38 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>emmii13</td>\n",
       "      <td>got to do my french and english h/w 2day  *ugh!*</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8599</th>\n",
       "      <td>0</td>\n",
       "      <td>1548278792</td>\n",
       "      <td>Fri Apr 17 20:31:10 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>Appletini6</td>\n",
       "      <td>Going to bed cause Melissa doesnt want to watc...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>29252</th>\n",
       "      <td>0</td>\n",
       "      <td>1562354667</td>\n",
       "      <td>Sun Apr 19 19:47:09 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>crystalgo</td>\n",
       "      <td>@_MissE_ ooh ok, i txted you a zillion times t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>61066</th>\n",
       "      <td>0</td>\n",
       "      <td>1686604427</td>\n",
       "      <td>Sun May 03 06:06:10 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>AQHA</td>\n",
       "      <td>#quarterfest Getting ready for last day of QF....</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       target         ids                          date      flag  \\\n",
       "10383       0  1550900222  Sat Apr 18 07:35:00 PDT 2009  NO_QUERY   \n",
       "22541       0  1557512136  Sun Apr 19 04:33:38 PDT 2009  NO_QUERY   \n",
       "8599        0  1548278792  Fri Apr 17 20:31:10 PDT 2009  NO_QUERY   \n",
       "29252       0  1562354667  Sun Apr 19 19:47:09 PDT 2009  NO_QUERY   \n",
       "61066       0  1686604427  Sun May 03 06:06:10 PDT 2009  NO_QUERY   \n",
       "\n",
       "                user                                               text  \n",
       "10383  amazingphoebe       MY INTERNET IS SOMEWHAT WORKING! I want seb   \n",
       "22541        emmii13   got to do my french and english h/w 2day  *ugh!*  \n",
       "8599      Appletini6  Going to bed cause Melissa doesnt want to watc...  \n",
       "29252      crystalgo  @_MissE_ ooh ok, i txted you a zillion times t...  \n",
       "61066           AQHA  #quarterfest Getting ready for last day of QF....  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Importing the dataset\n",
    "DATASET_COLUMNS=['target','ids','date','flag','user','text']\n",
    "DATASET_ENCODING = \"ISO-8859-1\"\n",
    "df = pd.read_csv(r\"C:\\Users\\vinne\\OneDrive\\Desktop\\training.vinay.csv\", encoding=DATASET_ENCODING, names=DATASET_COLUMNS)\n",
    "df.sample(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "259a2f03-e884-4483-8863-1c594a401a6e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>target</th>\n",
       "      <th>ids</th>\n",
       "      <th>date</th>\n",
       "      <th>flag</th>\n",
       "      <th>user</th>\n",
       "      <th>text</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1467810369</td>\n",
       "      <td>Mon Apr 06 22:19:45 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>_TheSpecialOne_</td>\n",
       "      <td>@switchfoot http://twitpic.com/2y1zl - Awww, t...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0</td>\n",
       "      <td>1467810672</td>\n",
       "      <td>Mon Apr 06 22:19:49 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>scotthamilton</td>\n",
       "      <td>is upset that he can't update his Facebook by ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>1467810917</td>\n",
       "      <td>Mon Apr 06 22:19:53 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>mattycus</td>\n",
       "      <td>@Kenichan I dived many times for the ball. Man...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>1467811184</td>\n",
       "      <td>Mon Apr 06 22:19:57 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>ElleCTF</td>\n",
       "      <td>my whole body feels itchy and like its on fire</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>1467811193</td>\n",
       "      <td>Mon Apr 06 22:19:57 PDT 2009</td>\n",
       "      <td>NO_QUERY</td>\n",
       "      <td>Karoli</td>\n",
       "      <td>@nationwideclass no, it's not behaving at all....</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   target         ids                          date      flag  \\\n",
       "0       0  1467810369  Mon Apr 06 22:19:45 PDT 2009  NO_QUERY   \n",
       "1       0  1467810672  Mon Apr 06 22:19:49 PDT 2009  NO_QUERY   \n",
       "2       0  1467810917  Mon Apr 06 22:19:53 PDT 2009  NO_QUERY   \n",
       "3       0  1467811184  Mon Apr 06 22:19:57 PDT 2009  NO_QUERY   \n",
       "4       0  1467811193  Mon Apr 06 22:19:57 PDT 2009  NO_QUERY   \n",
       "\n",
       "              user                                               text  \n",
       "0  _TheSpecialOne_  @switchfoot http://twitpic.com/2y1zl - Awww, t...  \n",
       "1    scotthamilton  is upset that he can't update his Facebook by ...  \n",
       "2         mattycus  @Kenichan I dived many times for the ball. Man...  \n",
       "3          ElleCTF    my whole body feels itchy and like its on fire   \n",
       "4           Karoli  @nationwideclass no, it's not behaving at all....  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "2c761669-7904-4ef4-b4dc-aabbe4c35497",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['target', 'ids', 'date', 'flag', 'user', 'text'], dtype='object')"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.columns\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "621fbf74-d596-4d48-95e4-698aaa81eb42",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['target', 'ids', 'date', 'flag', 'user', 'text'], dtype='object')"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.columns\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "9e598c89-40a5-4c03-8d20-ae1fd2a869e3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 65536 entries, 0 to 65535\n",
      "Data columns (total 6 columns):\n",
      " #   Column  Non-Null Count  Dtype \n",
      "---  ------  --------------  ----- \n",
      " 0   target  65536 non-null  int64 \n",
      " 1   ids     65536 non-null  int64 \n",
      " 2   date    65536 non-null  object\n",
      " 3   flag    65536 non-null  object\n",
      " 4   user    65536 non-null  object\n",
      " 5   text    65536 non-null  object\n",
      "dtypes: int64(2), object(4)\n",
      "memory usage: 3.0+ MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "03863804-307d-40a5-8a43-60d08ca5023f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "target     int64\n",
       "ids        int64\n",
       "date      object\n",
       "flag      object\n",
       "user      object\n",
       "text      object\n",
       "dtype: object"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "df.dtypes\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "50f1f8eb-b5dd-4d96-ad49-72053672d19b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.sum(df.isnull().any(axis=1))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "32e63fb7-9841-4e10-86f6-eb21ef6fb2fb",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Count of columns in the data is:   6\n",
      "Count of rows in the data is:   65536\n"
     ]
    }
   ],
   "source": [
    "print('Count of columns in the data is:  ', len(df.columns))\n",
    "print('Count of rows in the data is:  ', len(df))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "753d424f-6cea-4750-a85f-77f0340b7f86",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0, 4], dtype=int64)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['target'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "6d1a3ee5-3f06-4d90-a0a3-baee1efc9494",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "2"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['target'].nunique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "3a9801d7-2e7e-4467-82b3-468b2ee5db6b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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tKZ0HgAAcHmrUMgZNmyYvv76a7388svatm2bZs6cqTfffFNJSUmSJDc3Nw0dOlR///vfNW/ePG3YsEEPP/ywgoOD1b17d0m/nfm54447NHDgQK1evVorVqxQcnKyevXqpeDgYElSnz595OnpqcTERG3cuFGzZs3SpEmTlJKSYq/liSeeUEZGhsaNG6fNmzdr9OjRWrt2rZKTky/SoQEAANVZjYoUX3/99frkk080cuRIjRkzRmFhYZo4caL69u1r1wwfPlzHjh3ToEGDlJ+fr5tuukkZGRny9va2az788EMlJyfrtttuk7u7u3r06KHJkyfb/QEBAVq0aJGSkpLUrl071a9fX6mpqS7P0unYsaNmzpyp559/Xs8++6yaN2+uuXPn6tprr72Q4wEAAAxRoefkmIbn5FQenpNz7nhODgBUTKU8JwcAAKC6IOQAAAAjEXIAAICRCDkAAMBIhBwAAGAkQg4AADASIQcAABiJkAMAAIxEyAEAAEYi5AAAACMRcgAAgJEIOQAAwEiEHAAAYCRCDgAAMBIhBwAAGImQAwAAjETIAQAARiLkAAAAIxFyAACAkQg5AADASIQcAABgJEIOAAAwEiEHAAAYiZADAACMRMgBAABGIuQAAAAjEXIAAICRCDkAAMBIhBwAAGAkQg4AADASIQcAABiJkAMAAIxEyAEAAEYi5AAAACMRcgAAgJEIOQAAwEiEHAAAYCRCDgAAMBIhBwAAGImQAwAAjETIAQAARiLkAAAAIxFyAACAkSoUckaPHi03NzeXrWXLlnb/iRMnlJSUpHr16snf3189evRQXl6eyxi7d+9WXFycfH191bBhQz399NM6deqUS83SpUvVtm1beXl5qVmzZkpPTy+zlqlTp6pp06by9vZWVFSUVq9eXZG3AgAADFfhMznXXHON9u3bZ29fffWV3Tds2DB99tlnmjNnjpYtW6a9e/fqvvvus/uLi4sVFxenoqIirVy5UjNmzFB6erpSU1Ptmh07diguLk6dO3fW+vXrNXToUA0YMEALFy60a2bNmqWUlBSNGjVK69atU5s2bRQbG6v9+/ef73EAAACGqXDIqVGjhoKCguytfv36kqSCggL961//0vjx49WlSxe1a9dO7777rlauXKmvv/5akrRo0SJt2rRJH3zwgSIjI9WtWze9+OKLmjp1qoqKiiRJaWlpCgsL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kIMq0b9/f7m5uemVV15xaZ87d+6f/vTp9PT0ch8KuWbNGg0aNOhPXQtgotLPu5ubmzw9PdWsWTONGTNGp06duqBxO3bsqH379tkPheOzjN8j5KDKeHt769VXX9Xhw4ereinlatCggXx9fat6GYAR7rjjDu3bt08//PCDnnzySY0ePVqvv/76BY3p6empoKCgs/7DiM/y5YuQgyoTExOjoKAgjR079ow1X331lW6++Wb5+PgoJCREQ4YM0bFj//dbu/ft26e4uDj5+PgoLCxMM2fOLHNqevz48YqIiJCfn59CQkL02GOP6ejRo5J+O92dkJCggoIC+1+ao0ePluR6irtPnz7q2bOny9pOnjyp+vXr67333pP0268VGTt2rMLCwuTj46M2bdro448/vghHCqj+vLy8FBQUpNDQUA0ePFgxMTGaN2+eDh8+rIcfflh16tSRr6+vunXrph9++MHeb9euXbr77rtVp04d+fn56ZprrtHnn38uyfXrKj7LKA8hB1XGw8NDL7/8st544w399NNPZfq3b9+uO+64Qz169NC3336rWbNm6auvvnJ5+OPDDz+svXv3aunSpfr3v/+tN998U/v373cZx93dXZMnT9bGjRs1Y8YMZWVlafjw4ZJ+O909ceJEORwO7du3T/v27dNTTz1VZi19+/bVZ599ZocjSVq4cKF+/fVX/eUvf5H022+5f++995SWlqaNGzdq2LBheuihh7Rs2bKLcrwAk/j4+KioqEj9+/fX2rVrNW/ePGVnZ8uyLN155506efKkJCkpKUmFhYVavny5NmzYoFdffVX+/v5lxuOzjHJZQBWIj4+37r33XsuyLKtDhw7WI488YlmWZX3yySdW6R/LxMREa9CgQS77/fe//7Xc3d2t48ePW99//70lyVqzZo3d/8MPP1iSrAkTJpxx7jlz5lj16tWzX7/77rtWQEBAmbrQ0FB7nJMnT1r169e33nvvPbu/d+/eVs+ePS3LsqwTJ05Yvr6+1sqVK13GSExMtHr37v3HBwMw3Omf95KSEmvx4sWWl5eX1b17d0uStWLFCrv24MGDlo+PjzV79mzLsiwrIiLCGj16dLnjLlmyxJJkHT582LIsPssoq9r/WgdUf6+++qq6dOlS5l9d33zzjb799lt9+OGHdptlWSopKdGOHTu0detW1ahRQ23btrX7mzVrpjp16riM8+WXX2rs2LHavHmznE6nTp06pRMnTujXX3895+/pa9SooQcffFAffvih+vXrp2PHjunTTz/VRx99JEnatm2bfv31V91+++0u+xUVFem6666r0PEATDR//nz5+/vr5MmTKikpUZ8+fXTfffdp/vz5ioqKsuvq1aunFi1a6Pvvv5ckDRkyRIMHD9aiRYsUExOjHj16qHXr1ue9Dj7LlxdCDqrcLbfcotjYWI0cOVL9+/e3248ePaq//vWvGjJkSJl9mjRpoq1bt5517J07d+quu+7S4MGD9dJLL6lu3br66quvlJiYqKKiogpdjNi3b1/deuut2r9/vxYvXiwfHx/dcccd9lolacGCBbriiitc9uN36QBS586dNX36dHl6eio4OFg1atTQvHnzzrrfgAEDFBsbqwULFmjRokUaO3asxo0bp8cff/y818Jn+fJByMEl4ZVXXlFkZKRatGhht7Vt21abNm1Ss2bNyt2nRYsWOnXqlP73v/+pXbt2kn77V9jpd2vl5OSopKRE48aNk7v7b5egzZ4922UcT09PFRcXn3WNHTt2VEhIiGbNmqUvvvhCDzzwgGrWrClJCg8Pl5eXl3bv3q1bb721Ym8euAz4+fmV+Sy3atVKp06d0qpVq9SxY0dJ0i+//KItW7YoPDzcrgsJCdGjjz6qRx99VCNHjtRbb71Vbsjhs4zfI+TgkhAREaG+fftq8uTJdtszzzyjDh06KDk5WQMGDJCfn582bdqkxYsXa8qUKWrZsqViYmI0aNAgTZ8+XTVr1tSTTz4pHx8f+5bSZs2a6eTJk3rjjTd09913a8WKFUpLS3OZu2nTpjp69KgyMzPVpk0b+fr6nvEMT58+fZSWlqatW7dqyZIldnutWrX01FNPadiwYSopKdFNN92kgoICrVixQg6HQ/Hx8ZVw1IDqrXnz5rr33ns1cOBA/fOf/1StWrU0YsQIXXHFFbr33nslSUOHDlW3bt109dVX6/Dhw1qyZIlatWpV7nh8llFGVV8UhMvT6RciltqxY4fl6elpnf7HcvXq1dbtt99u+fv7W35+flbr1q2tl156ye7fu3ev1a1bN8vLy8sKDQ21Zs6caTVs2NBKS0uza8aPH281atTI8vHxsWJjY6333nvP5WJFy7KsRx991KpXr54lyRo1apRlWa4XK5batGmTJckKDQ21SkpKXPpKSkqsiRMnWi1atLBq1qxpNWjQwIqNjbWWLVt2YQcLqObK+7yXOnTokNWvXz8rICDA/oxu3brV7k9OTrauuuoqy8vLy2rQoIHVr18/6+DBg5Zllb3w2LL4LMOVm2VZVhVmLOCi+umnnxQSEqIvv/xSt912W1UvBwBQhQg5qNaysrJ09OhRRUREaN++fRo+fLh+/vlnbd261f6OHQBweeKaHFRrJ0+e1LPPPqsff/xRtWrVUseOHfXhhx8ScAAAnMkBAABm4tc6AAAAIxFyAACAkQg5AADASIQcAABgJEIOAAAwEiEHwCWjU6dOGjp0aFUvw3aprQdAxRByABilqKioqpcA4BJByAFwSejfv7+WLVumSZMmyc3NTW5ubtq+fbsSExMVFhYmHx8ftWjRQpMmTSqzX/fu3fXSSy8pODjY/k32K1euVGRkpLy9vdW+fXvNnTtXbm5uWr9+vb3vd999p27dusnf31+BgYHq16+fDh48eMb17Ny58886HAAuAp54DOCSMGnSJG3dulXXXnutxowZI0mqU6eOGjdurDlz5qhevXpauXKlBg0apEaNGunBBx+0983MzJTD4dDixYslSU6nU3fffbfuvPNOzZw5U7t27SrztVN+fr66dOmiAQMGaMKECTp+/LieeeYZPfjgg8rKyip3PQ0aNPhzDgaAi4KQA+CSEBAQIE9PT/n6+iooKMhuf+GFF+z/DgsLU3Z2tmbPnu0Scvz8/PT222/L09NTkpSWliY3Nze99dZb8vb2Vnh4uH7++WcNHDjQ3mfKlCm67rrr9PLLL9tt77zzjkJCQrR161ZdffXV5a4HQPVByAFwSZs6dareeecd7d69W8ePH1dRUZEiIyNdaiIiIuyAI0lbtmxR69at5e3tbbfdcMMNLvt88803WrJkifz9/cvMuX37dl199dUX940A+NMRcgBcsj766CM99dRTGjdunKKjo1WrVi29/vrrWrVqlUudn59fhcc+evSo7r77br366qtl+ho1anTeawZw6SDkALhkeHp6qri42H69YsUKdezYUY899pjdtn379rOO06JFC33wwQcqLCyUl5eXJGnNmjUuNW3bttW///1vNW3aVDVqlP9X4e/XA6B64e4qAJeMpk2batWqVdq5c6cOHjyo5s2ba+3atVq4cKG2bt2qv/3tb2XCSnn69OmjkpISDRo0SN9//70WLlyof/zjH5IkNzc3SVJSUpIOHTqk3r17a82aNdq+fbsWLlyohIQEO9j8fj0lJSWV9+YBXHSEHACXjKeeekoeHh4KDw9XgwYNFBsbq/vuu089e/ZUVFSUfvnlF5ezOmficDj02Wefaf369YqMjNRzzz2n1NRUSbKv0wkODtaKFStUXFysrl27KiIiQkOHDlXt2rXl7u5e7np2795deW8ewEXnZlmWVdWLAIDK9uGHHyohIUEFBQXy8fGp6uUA+BNwTQ4AI7333nu68sordcUVV+ibb76xn4FDwAEuH4QcAEbKzc1VamqqcnNz1ahRIz3wwAN66aWXqnpZAP5EfF0FAACMxIXHAADASIQcAABgJEIOAAAwEiEHAAAYiZADAACMRMgBAABGIuQAAAAjEXIAAICRCDkAAMBI/x9Xo2jfr0RexgAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "# Plotting the distribution for dataset.\n",
    "ax = df.groupby('target').count().plot(kind='bar', title='Distribution of data',legend=False)\n",
    "ax.set_xticklabels(['Negative','Positive'], rotation=0)\n",
    "# Storing data in lists.\n",
    "text, sentiment = list(df['text']), list(df['target'])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "a6438de3-f8b3-4ca0-a3bf-dc1b05281b28",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: xlabel='target', ylabel='count'>"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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iRN/+hMDAACCTkBD08qVKyVJd9xxh9/4f/3Xf+kXv/iFJGnx4sUKCQnRmDFjVFtbK7fbrRUrVli1oaGh2rRpk6ZMmSKXy6XOnTsrLS1N8+fPt2r69u2rvLw8TZ8+XUuXLlXv3r315ptvyu12WzVjx45VZWWlsrOz5fV6lZCQoPz8/GY3hwMAgKtTUD2nqT27mOc8XAqe0wQ0x3OaALRWu31OEwAAQLAiNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABggNAEAABgIaGjasWOHHnjgAcXGxspms2nDhg1+842NjcrOzlavXr0UERGhlJQUffHFF341J0+e1IQJE+RwOBQZGan09HSdPn3ar+aTTz7RbbfdpvDwcMXFxWnhwoXNelm/fr0GDBig8PBwDR48WH/605/a/HgBAED7FdDQVFNTo6FDh2r58uUtzi9cuFCvvvqqcnJytHv3bnXu3Flut1tnz561aiZMmKBDhw5p69at2rRpk3bs2KHJkydb8z6fT6NGjdJ1112n4uJiLVq0SPPmzdPrr79u1ezatUvjx49Xenq6PvroI40ePVqjR4/WwYMHL9/BAwCAdsXW2NjYGOgmJMlms+ndd9/V6NGjJf3zKlNsbKyeeeYZPfvss5Kk6upqRUdHKzc3V+PGjdNnn32m+Ph47d27V0lJSZKk/Px83Xffffrqq68UGxurlStX6rnnnpPX65XdbpckzZo1Sxs2bFBpaakkaezYsaqpqdGmTZusfkaOHKmEhATl5OQY9e/z+eR0OlVdXS2Hw9FWp6WZxBlvXba1gfaqeNHjgW4BQDt1Mb+/g/aepqNHj8rr9SolJcUaczqdSk5OVlFRkSSpqKhIkZGRVmCSpJSUFIWEhGj37t1Wze23324FJklyu906fPiwTp06ZdVcuJ+m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aAIAADBAaAIAADBAaAIAADBAaAIAADBAaAJwRbrjjjuUmZkZ6DYswdYPgItHaAKA71FXVxfoFgAEEUITgCvOL37xCxUWFmrp0qWy2Wyy2Ww6cuSI0tPT1bdvX0VERKh///5aunRps/eNHj1aL774omJjY9W/f39J0q5du5SQkKDw8HAlJSVpw4YNstlsKikpsd578OBB3XvvverSpYuio6P12GOP6cSJE9/bz5dffvlTnQ4AbaRDoBsAgLa2dOlSff755xo0aJDmz58vSbrmmmvUu3dvrV+/Xt27d9euXbs0efJk9erVS4888oj13oKCAjkcDm3dulWS5PP59MADD+i+++7TmjVr9L//+7/NPmarqqrSXXfdpSeffFKLFy/WmTNnlJWVpUceeUTbtm1rsZ+oqKif5mQAaDOEJgBXHKfTKbvdrk6dOikmJsYaf/75561/9+3bV0VFRVq3bp1faOrcubPefPNN2e12SVJOTo5sNpveeOMNhYeHKz4+Xn//+981adIk6z3Lli3TTTfdpJdeeskaW7VqleLi4vT555/rxhtvbLEfAO0LoQnAVWP58uVatWqVysrKdObMGdXV1SkhIcGvZvDgwVZgkqTDhw9ryJAhCg8Pt8ZGjBjh956PP/5YH3zwgbp06dJsn0eOHNGNN97YtgcCICAITQCuCu+8846effZZvfLKK3K5XOratasWLVqk3bt3+9V17tz5otc+ffq0HnjgAf32t79tNterV69W9wwguBCaAFyR7Ha76uvrrdc7d+7UzTffrF/+8pfW2JEjR350nf79++u///u/VVtbq7CwMEnS3r17/WqGDRumP/zhD+rTp486dGj5v9Xv9gOg/eHbcwCuSH369NHu3bv15Zdf6sSJE7rhhhu0b98+bdmyRZ9//rl+85vfNAs/LXn00UfV0NCgyZMn67PPPtOWLVv0n//5n5Ikm80mScrIyNDJkyc1fvx47d27V0eOHNGWLVs0ceJEKyh9t5+GhobLd/AALgtCE4Ar0rPPPqvQ0FDFx8crKipKbrdbDz74oMaOHavk5GR98803fledvo/D4dDGjRtVUlKihIQEPffcc8rOzpYk6z6n2NhY7dy5U/X19Ro1apQGDx6szMxMRUZGKiQkpMV+ysrKLt/BA7gsbI2NjY2BbgIA2pO3335bEydOVHV1tSIiIgLdDoCfCPc0AcCPeOutt3T99dfrZz/7mT7++GPrGUwEJuDqQmgCgB/h9XqVnZ0tr9erXr166eGHH9aLL74Y6LYA/MT4eA4AAMAAN4IDAAAYIDQBAAAYIDQBAAAYIDQBAAAYIDQBAAAYIDQBAAAYIDQBAAAYIDQBAAAY+D81MPb7mS+m7gAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 640x480 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import seaborn as sns\n",
    "sns.countplot(x='target', data=df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "86272be1-bdac-4cea-82f2-8f57afe26b53",
   "metadata": {},
   "outputs": [],
   "source": [
    "data=df[['text','target']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "e5f95a19-e5ad-41eb-9372-08fff00a0aa8",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_pos = data[data['target'] == 1]\n",
    "data_neg = data[data['target'] == 0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "0b1cebdb-8341-4c0b-93fb-ac3fc4851a12",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_pos = data_pos.iloc[:int(20000)]\n",
    "data_neg = data_neg.iloc[:int(20000)]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "6e7b91cb-309e-46b8-935c-e34ec0c87b96",
   "metadata": {},
   "outputs": [],
   "source": [
    "dataset = pd.concat([data_pos, data_neg])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "bb57561b-ac4a-454a-98dc-b7773e6febd3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "19995    not much time off this weekend, work trip to m...\n",
       "19996                            one more day of holidays \n",
       "19997    feeling so down right now .. i hate you damn h...\n",
       "19998    geez,i hv to read the whole book of personalit...\n",
       "19999    i threw my sign at donnie and he bent over to ...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "dataset['text']=dataset['text'].str.lower()\n",
    "dataset['text'].tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "4703853f-6391-4e68-9aa4-eca9b0dfb719",
   "metadata": {},
   "outputs": [],
   "source": [
    "stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',\n",
    "             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',\n",
    "             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',\n",
    "             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',\n",
    "             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',\n",
    "             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',\n",
    "             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',\n",
    "             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',\n",
    "             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', \"shes\", 'should', \"shouldve\",'so', 'some', 'such',\n",
    "             't', 'than', 'that', \"thatll\", 'the', 'their', 'theirs', 'them',\n",
    "             'themselves', 'then', 'there', 'these', 'they', 'this', 'those',\n",
    "             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',\n",
    "             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',\n",
    "             'why', 'will', 'with', 'won', 'y', 'you', \"youd\",\"youll\", \"youre\",\n",
    "             \"youve\", 'your', 'yours', 'yourself', 'yourselves']\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "f83fde16-e533-4ed7-aea8-a9f8c39448c1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    @switchfoot http://twitpic.com/2y1zl - awww, t...\n",
       "1    upset can't update facebook texting it... migh...\n",
       "2    @kenichan dived many times ball. managed save ...\n",
       "3                     whole body feels itchy like fire\n",
       "4    @nationwideclass no, it's not behaving all. i'...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "STOPWORDS = set(stopwordlist)\n",
    "def cleaning_stopwords(text):\n",
    "    return \" \".join([word for word in str(text).split() if word not in STOPWORDS])\n",
    "dataset['text'] = dataset['text'].apply(lambda text: cleaning_stopwords(text))\n",
    "dataset['text'].head()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "e978cf75-9514-46a2-87e0-01d605df0d17",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "19995    not much time off weekend work trip malm frisa...\n",
       "19996                                     one day holidays\n",
       "19997                     feeling right  hate damn humprey\n",
       "19998    geezi hv read whole book personality types emb...\n",
       "19999    threw sign donnie bent over get but thingee ma...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import string\n",
    "english_punctuations = string.punctuation\n",
    "punctuations_list = english_punctuations\n",
    "def cleaning_punctuations(text):\n",
    "    translator = str.maketrans('', '', punctuations_list)\n",
    "    return text.translate(translator)\n",
    "dataset['text']= dataset['text'].apply(lambda x: cleaning_punctuations(x))\n",
    "dataset['text'].tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "76adf281-c901-4239-9334-cae2435d1fd2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "19995    not much time off weekend work trip malm frisa...\n",
       "19996                                     one day holidays\n",
       "19997                     feeling right  hate damn humprey\n",
       "19998    geezi hv read whole book personality types emb...\n",
       "19999    threw sign donnie bent over get but thingee ma...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def cleaning_repeating_char(text):\n",
    "    return re.sub(r'(.)1+', r'1', text)\n",
    "dataset['text'] = dataset['text'].apply(lambda x: cleaning_repeating_char(x))\n",
    "dataset['text'].tail()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "9a66aad7-a7ba-491e-baf9-7b913695d6a9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "19995    not much time off weekend work trip malm frisa...\n",
       "19996                                     one day holidays\n",
       "19997                     feeling right  hate damn humprey\n",
       "19998    geezi hv read whole book personality types emb...\n",
       "19999    threw sign donnie bent over get but thingee ma...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def cleaning_URLs(data):\n",
    "    return re.sub('((www.[^s]+)|(https?://[^s]+))',' ',data)\n",
    "dataset['text'] = dataset['text'].apply(lambda x: cleaning_URLs(x))\n",
    "dataset['text'].tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "0ef0f7da-15f6-42e9-a574-af763bb64fca",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "19995    not much time off weekend work trip malm frisa...\n",
       "19996                                     one day holidays\n",
       "19997                     feeling right  hate damn humprey\n",
       "19998    geezi hv read whole book personality types emb...\n",
       "19999    threw sign donnie bent over get but thingee ma...\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def cleaning_numbers(data):\n",
    "    return re.sub('[0-9]+', '', data)\n",
    "dataset['text'] = dataset['text'].apply(lambda x: cleaning_numbers(x))\n",
    "dataset['text'].tail()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "648af94f-432c-417a-90d3-24d908972846",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    [w, w]\n",
       "1        []\n",
       "2        []\n",
       "3       [w]\n",
       "4       [w]\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from nltk.tokenize import RegexpTokenizer\n",
    "tokenizer = RegexpTokenizer(r'w+')\n",
    "dataset['text'] = dataset['text'].apply(tokenizer.tokenize)\n",
    "dataset['text'].head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "9c713592-f1bb-4a26-8c78-3b460a9e871c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    [w, w]\n",
       "1        []\n",
       "2        []\n",
       "3       [w]\n",
       "4       [w]\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import nltk\n",
    "st = nltk.PorterStemmer()\n",
    "def stemming_on_text(data):\n",
    "    text = [st.stem(word) for word in data]\n",
    "    return data\n",
    "dataset['text']= dataset['text'].apply(lambda x: stemming_on_text(x))\n",
    "dataset['text'].head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "c51fc5a2-21b7-458a-864f-fa0dc9417374",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    [w, w]\n",
       "1        []\n",
       "2        []\n",
       "3       [w]\n",
       "4       [w]\n",
       "Name: text, dtype: object"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lm = nltk.WordNetLemmatizer()\n",
    "def lemmatizer_on_text(data):\n",
    "    text = [lm.lemmatize(word) for word in data]\n",
    "    return data\n",
    "dataset['text'] = dataset['text'].apply(lambda x: lemmatizer_on_text(x))\n",
    "dataset['text'].head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "af00aa24-e37d-4f70-8d2d-ba42d0668284",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "X=data.text\n",
    "y=data.target"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "4d7b7858-5683-445f-887e-98430cb6202d",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x263113fa510>"
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "text/plain": [
       "<Figure size 2000x2000 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "data_neg = data['text'][:800000]\n",
    "plt.figure(figsize = (20,20))\n",
    "wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,\n",
    "               collocations=False).generate(\" \".join(data_neg))\n",
    "plt.imshow(wc)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "61d28abb-b301-4fe4-951f-83f3752ea34f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.image.AxesImage at 0x263173002f0>"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "text/plain": [
       "<Figure size 2000x2000 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "data_pos = data['text'][50000:]\n",
    "wc = WordCloud(max_words = 1000 , width = 1600 , height = 800,\n",
    "              collocations=False).generate(\" \".join(data_pos))\n",
    "plt.figure(figsize = (20,20))\n",
    "plt.imshow(wc)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "bd5e8646-58e0-431d-969a-ac6e0bde557b",
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.05, random_state =26105111)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "181701f1-c501-476c-9435-9928dbc02a0a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "           0       1.00      1.00      1.00      3277\n",
      "\n",
      "    accuracy                           1.00      3277\n",
      "   macro avg       1.00      1.00      1.00      3277\n",
      "weighted avg       1.00      1.00      1.00      3277\n",
      "\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\vinne\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\metrics\\_classification.py:386: UserWarning: A single label was found in 'y_true' and 'y_pred'. For the confusion matrix to have the correct shape, use the 'labels' parameter to pass all known labels.\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "ename": "ValueError",
     "evalue": "cannot reshape array of size 1 into shape (2,2)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[53], line 49\u001b[0m\n\u001b[0;32m     46\u001b[0m BNBmodel\u001b[38;5;241m.\u001b[39mfit(X_train_transformed, y_train)\n\u001b[0;32m     48\u001b[0m \u001b[38;5;66;03m# Evaluate the model\u001b[39;00m\n\u001b[1;32m---> 49\u001b[0m \u001b[43mmodel_Evaluate\u001b[49m\u001b[43m(\u001b[49m\u001b[43mBNBmodel\u001b[49m\u001b[43m,\u001b[49m\u001b[43mX_test_transformed\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43my_test\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m     51\u001b[0m \u001b[38;5;66;03m# Optionally, you can also get predictions separately\u001b[39;00m\n\u001b[0;32m     52\u001b[0m y_pred1 \u001b[38;5;241m=\u001b[39m BNBmodel\u001b[38;5;241m.\u001b[39mpredict(X_test_transformed)\n",
      "Cell \u001b[1;32mIn[53], line 31\u001b[0m, in \u001b[0;36mmodel_Evaluate\u001b[1;34m(model, X_test, y_test)\u001b[0m\n\u001b[0;32m     29\u001b[0m group_percentages \u001b[38;5;241m=\u001b[39m [\u001b[38;5;124m'\u001b[39m\u001b[38;5;132;01m{0:.2%}\u001b[39;00m\u001b[38;5;124m'\u001b[39m\u001b[38;5;241m.\u001b[39mformat(value) \u001b[38;5;28;01mfor\u001b[39;00m value \u001b[38;5;129;01min\u001b[39;00m cf_matrix\u001b[38;5;241m.\u001b[39mflatten() \u001b[38;5;241m/\u001b[39m np\u001b[38;5;241m.\u001b[39msum(cf_matrix)]\n\u001b[0;32m     30\u001b[0m labels \u001b[38;5;241m=\u001b[39m [\u001b[38;5;124mf\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mv1\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124mn\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mv2\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m'\u001b[39m \u001b[38;5;28;01mfor\u001b[39;00m v1, v2 \u001b[38;5;129;01min\u001b[39;00m \u001b[38;5;28mzip\u001b[39m(group_names,group_percentages)]\n\u001b[1;32m---> 31\u001b[0m labels   \u001b[38;5;241m=\u001b[39m \u001b[43mnp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43masarray\u001b[49m\u001b[43m(\u001b[49m\u001b[43mlabels\u001b[49m\u001b[43m)\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mreshape\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;241;43m2\u001b[39;49m\u001b[43m,\u001b[49m\u001b[38;5;241;43m2\u001b[39;49m\u001b[43m)\u001b[49m\n\u001b[0;32m     32\u001b[0m plt\u001b[38;5;241m.\u001b[39mfigure(figsize\u001b[38;5;241m=\u001b[39m(\u001b[38;5;241m8\u001b[39m, \u001b[38;5;241m6\u001b[39m))\n\u001b[0;32m     33\u001b[0m sns\u001b[38;5;241m.\u001b[39mheatmap(cf_matrix, annot \u001b[38;5;241m=\u001b[39m labels, cmap \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mBlues\u001b[39m\u001b[38;5;124m'\u001b[39m,fmt \u001b[38;5;241m=\u001b[39m \u001b[38;5;124m'\u001b[39m\u001b[38;5;124m'\u001b[39m,\n\u001b[0;32m     34\u001b[0m xticklabels \u001b[38;5;241m=\u001b[39m categories, yticklabels \u001b[38;5;241m=\u001b[39m categories)\n",
      "\u001b[1;31mValueError\u001b[0m: cannot reshape array of size 1 into shape (2,2)"
     ]
    }
   ],
   "source": [
    "from sklearn.feature_extraction.text import CountVectorizer\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.naive_bayes import BernoulliNB\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "def preprocess_text_data(X_train, X_test):\n",
    "    # Initialize CountVectorizer to convert text data into numerical format\n",
    "    vectorizer = CountVectorizer(binary=True)\n",
    "    \n",
    "    # Fit and transform the training data\n",
    "    X_train_transformed = vectorizer.fit_transform(X_train)\n",
    "    \n",
    "    # Transform the test data using the same vectorizer\n",
    "    X_test_transformed = vectorizer.transform(X_test)\n",
    "    \n",
    "    return X_train_transformed, X_test_transformed\n",
    "\n",
    "def model_Evaluate(model, X_test, y_test):\n",
    "    # Predict values for Test dataset\n",
    "    y_pred = model.predict(X_test)\n",
    "    # Print the evaluation metrics for the dataset.\n",
    "    print(classification_report(y_test, y_pred))\n",
    "    # Compute and plot the Confusion matrix\n",
    "    cf_matrix = confusion_matrix(y_test, y_pred)\n",
    "    categories = ['Negative','Positive']\n",
    "    group_names = ['True Neg','False Pos', 'False Neg','True Pos']\n",
    "    group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten() / np.sum(cf_matrix)]\n",
    "    labels = [f'{v1}n{v2}' for v1, v2 in zip(group_names,group_percentages)]\n",
    "    labels   = np.asarray(labels).reshape(2,2)\n",
    "    plt.figure(figsize=(8, 6))\n",
    "    sns.heatmap(cf_matrix, annot = labels, cmap = 'Blues',fmt = '',\n",
    "    xticklabels = categories, yticklabels = categories)\n",
    "    plt.xlabel(\"Predicted values\", fontdict = {'size':14}, labelpad = 10)\n",
    "    plt.ylabel(\"Actual values\" , fontdict = {'size':14}, labelpad = 10)\n",
    "    plt.title (\"Confusion Matrix\", fontdict = {'size':18}, pad = 20)\n",
    "    plt.show()\n",
    "\n",
    "# Assuming X_train, X_test, y_train, and y_test are defined before calling this code\n",
    "# Preprocess text data\n",
    "X_train_transformed, X_test_transformed = preprocess_text_data(X_train, X_test)\n",
    "\n",
    "# Initialize and fit the model\n",
    "BNBmodel = BernoulliNB()\n",
    "BNBmodel.fit(X_train_transformed, y_train)\n",
    "\n",
    "# Evaluate the model\n",
    "model_Evaluate(BNBmodel,X_test_transformed, y_test)\n",
    "\n",
    "# Optionally, you can also get predictions separately\n",
    "y_pred1 = BNBmodel.predict(X_test_transformed)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "id": "5a05aa68-28bb-4c1b-ba03-bd4af6010086",
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'y_pred1' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[54], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01msklearn\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mmetrics\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m roc_curve, auc\n\u001b[1;32m----> 2\u001b[0m fpr, tpr, thresholds \u001b[38;5;241m=\u001b[39m roc_curve(y_test, \u001b[43my_pred1\u001b[49m)\n\u001b[0;32m      3\u001b[0m roc_auc \u001b[38;5;241m=\u001b[39m auc(fpr, tpr)\n\u001b[0;32m      4\u001b[0m plt\u001b[38;5;241m.\u001b[39mfigure()\n",
      "\u001b[1;31mNameError\u001b[0m: name 'y_pred1' is not defined"
     ]
    }
   ],
   "source": [
    "from sklearn.metrics import roc_curve, auc\n",
    "fpr, tpr, thresholds = roc_curve(y_test, y_pred1)\n",
    "roc_auc = auc(fpr, tpr)\n",
    "plt.figure()\n",
    "plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)\n",
    "plt.xlim([0.0, 1.0])\n",
    "plt.ylim([0.0, 1.05])\n",
    "plt.xlabel('False Positive Rate')\n",
    "plt.ylabel('True Positive Rate')\n",
    "plt.title('ROC CURVE')\n",
    "plt.legend(loc=\"lower right\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "0531092e-5990-455d-b9bc-fd631f5fac52",
   "metadata": {},
   "outputs": [
    {
     "ename": "ValueError",
     "evalue": "could not convert string to float: 'stayin in tonight... movie night... solo status '",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[55], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m SVCmodel \u001b[38;5;241m=\u001b[39m LinearSVC()\n\u001b[1;32m----> 2\u001b[0m \u001b[43mSVCmodel\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mfit\u001b[49m\u001b[43m(\u001b[49m\u001b[43mX_train\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43my_train\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m      3\u001b[0m model_Evaluate(SVCmodel)\n\u001b[0;32m      4\u001b[0m y_pred2 \u001b[38;5;241m=\u001b[39m SVCmodel\u001b[38;5;241m.\u001b[39mpredict(X_test)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\base.py:1474\u001b[0m, in \u001b[0;36m_fit_context.<locals>.decorator.<locals>.wrapper\u001b[1;34m(estimator, *args, **kwargs)\u001b[0m\n\u001b[0;32m   1467\u001b[0m     estimator\u001b[38;5;241m.\u001b[39m_validate_params()\n\u001b[0;32m   1469\u001b[0m \u001b[38;5;28;01mwith\u001b[39;00m config_context(\n\u001b[0;32m   1470\u001b[0m     skip_parameter_validation\u001b[38;5;241m=\u001b[39m(\n\u001b[0;32m   1471\u001b[0m         prefer_skip_nested_validation \u001b[38;5;129;01mor\u001b[39;00m global_skip_validation\n\u001b[0;32m   1472\u001b[0m     )\n\u001b[0;32m   1473\u001b[0m ):\n\u001b[1;32m-> 1474\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mfit_method\u001b[49m\u001b[43m(\u001b[49m\u001b[43mestimator\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\svm\\_classes.py:310\u001b[0m, in \u001b[0;36mLinearSVC.fit\u001b[1;34m(self, X, y, sample_weight)\u001b[0m\n\u001b[0;32m    285\u001b[0m \u001b[38;5;129m@_fit_context\u001b[39m(prefer_skip_nested_validation\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mTrue\u001b[39;00m)\n\u001b[0;32m    286\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mfit\u001b[39m(\u001b[38;5;28mself\u001b[39m, X, y, sample_weight\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mNone\u001b[39;00m):\n\u001b[0;32m    287\u001b[0m \u001b[38;5;250m    \u001b[39m\u001b[38;5;124;03m\"\"\"Fit the model according to the given training data.\u001b[39;00m\n\u001b[0;32m    288\u001b[0m \n\u001b[0;32m    289\u001b[0m \u001b[38;5;124;03m    Parameters\u001b[39;00m\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m    308\u001b[0m \u001b[38;5;124;03m        An instance of the estimator.\u001b[39;00m\n\u001b[0;32m    309\u001b[0m \u001b[38;5;124;03m    \"\"\"\u001b[39;00m\n\u001b[1;32m--> 310\u001b[0m     X, y \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_validate_data\u001b[49m\u001b[43m(\u001b[49m\n\u001b[0;32m    311\u001b[0m \u001b[43m        \u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m    312\u001b[0m \u001b[43m        \u001b[49m\u001b[43my\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m    313\u001b[0m \u001b[43m        \u001b[49m\u001b[43maccept_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mcsr\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m    314\u001b[0m \u001b[43m        \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mnp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mfloat64\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m    315\u001b[0m \u001b[43m        \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mC\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m    316\u001b[0m \u001b[43m        \u001b[49m\u001b[43maccept_large_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;28;43;01mFalse\u001b[39;49;00m\u001b[43m,\u001b[49m\n\u001b[0;32m    317\u001b[0m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    318\u001b[0m     check_classification_targets(y)\n\u001b[0;32m    319\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mclasses_ \u001b[38;5;241m=\u001b[39m np\u001b[38;5;241m.\u001b[39munique(y)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\base.py:650\u001b[0m, in \u001b[0;36mBaseEstimator._validate_data\u001b[1;34m(self, X, y, reset, validate_separately, cast_to_ndarray, **check_params)\u001b[0m\n\u001b[0;32m    648\u001b[0m         y \u001b[38;5;241m=\u001b[39m check_array(y, input_name\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124my\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mcheck_y_params)\n\u001b[0;32m    649\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 650\u001b[0m         X, y \u001b[38;5;241m=\u001b[39m \u001b[43mcheck_X_y\u001b[49m\u001b[43m(\u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43my\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mcheck_params\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    651\u001b[0m     out \u001b[38;5;241m=\u001b[39m X, y\n\u001b[0;32m    653\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m no_val_X \u001b[38;5;129;01mand\u001b[39;00m check_params\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mensure_2d\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mTrue\u001b[39;00m):\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\validation.py:1263\u001b[0m, in \u001b[0;36mcheck_X_y\u001b[1;34m(X, y, accept_sparse, accept_large_sparse, dtype, order, copy, force_all_finite, ensure_2d, allow_nd, multi_output, ensure_min_samples, ensure_min_features, y_numeric, estimator)\u001b[0m\n\u001b[0;32m   1258\u001b[0m         estimator_name \u001b[38;5;241m=\u001b[39m _check_estimator_name(estimator)\n\u001b[0;32m   1259\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[0;32m   1260\u001b[0m         \u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mestimator_name\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m requires y to be passed, but the target y is None\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[0;32m   1261\u001b[0m     )\n\u001b[1;32m-> 1263\u001b[0m X \u001b[38;5;241m=\u001b[39m \u001b[43mcheck_array\u001b[49m\u001b[43m(\u001b[49m\n\u001b[0;32m   1264\u001b[0m \u001b[43m    \u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1265\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43maccept_sparse\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1266\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_large_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43maccept_large_sparse\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1267\u001b[0m \u001b[43m    \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1268\u001b[0m \u001b[43m    \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1269\u001b[0m \u001b[43m    \u001b[49m\u001b[43mcopy\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mcopy\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1270\u001b[0m \u001b[43m    \u001b[49m\u001b[43mforce_all_finite\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mforce_all_finite\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1271\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_2d\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_2d\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1272\u001b[0m \u001b[43m    \u001b[49m\u001b[43mallow_nd\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mallow_nd\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1273\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_min_samples\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_min_samples\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1274\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_min_features\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_min_features\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1275\u001b[0m \u001b[43m    \u001b[49m\u001b[43mestimator\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mestimator\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1276\u001b[0m \u001b[43m    \u001b[49m\u001b[43minput_name\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mX\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1277\u001b[0m \u001b[43m\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m   1279\u001b[0m y \u001b[38;5;241m=\u001b[39m _check_y(y, multi_output\u001b[38;5;241m=\u001b[39mmulti_output, y_numeric\u001b[38;5;241m=\u001b[39my_numeric, estimator\u001b[38;5;241m=\u001b[39mestimator)\n\u001b[0;32m   1281\u001b[0m check_consistent_length(X, y)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\validation.py:997\u001b[0m, in \u001b[0;36mcheck_array\u001b[1;34m(array, accept_sparse, accept_large_sparse, dtype, order, copy, force_all_finite, ensure_2d, allow_nd, ensure_min_samples, ensure_min_features, estimator, input_name)\u001b[0m\n\u001b[0;32m    995\u001b[0m         array \u001b[38;5;241m=\u001b[39m xp\u001b[38;5;241m.\u001b[39mastype(array, dtype, copy\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mFalse\u001b[39;00m)\n\u001b[0;32m    996\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 997\u001b[0m         array \u001b[38;5;241m=\u001b[39m \u001b[43m_asarray_with_order\u001b[49m\u001b[43m(\u001b[49m\u001b[43marray\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mxp\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mxp\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    998\u001b[0m \u001b[38;5;28;01mexcept\u001b[39;00m ComplexWarning \u001b[38;5;28;01mas\u001b[39;00m complex_warning:\n\u001b[0;32m    999\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[0;32m   1000\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mComplex data not supported\u001b[39m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;132;01m{}\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;241m.\u001b[39mformat(array)\n\u001b[0;32m   1001\u001b[0m     ) \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mcomplex_warning\u001b[39;00m\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\_array_api.py:521\u001b[0m, in \u001b[0;36m_asarray_with_order\u001b[1;34m(array, dtype, order, copy, xp)\u001b[0m\n\u001b[0;32m    519\u001b[0m     array \u001b[38;5;241m=\u001b[39m numpy\u001b[38;5;241m.\u001b[39marray(array, order\u001b[38;5;241m=\u001b[39morder, dtype\u001b[38;5;241m=\u001b[39mdtype)\n\u001b[0;32m    520\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 521\u001b[0m     array \u001b[38;5;241m=\u001b[39m \u001b[43mnumpy\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43masarray\u001b[49m\u001b[43m(\u001b[49m\u001b[43marray\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    523\u001b[0m \u001b[38;5;66;03m# At this point array is a NumPy ndarray. We convert it to an array\u001b[39;00m\n\u001b[0;32m    524\u001b[0m \u001b[38;5;66;03m# container that is consistent with the input's namespace.\u001b[39;00m\n\u001b[0;32m    525\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m xp\u001b[38;5;241m.\u001b[39masarray(array)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pandas\\core\\series.py:1022\u001b[0m, in \u001b[0;36mSeries.__array__\u001b[1;34m(self, dtype)\u001b[0m\n\u001b[0;32m    975\u001b[0m \u001b[38;5;250m\u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m    976\u001b[0m \u001b[38;5;124;03mReturn the values as a NumPy array.\u001b[39;00m\n\u001b[0;32m    977\u001b[0m \n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m   1019\u001b[0m \u001b[38;5;124;03m      dtype='datetime64[ns]')\u001b[39;00m\n\u001b[0;32m   1020\u001b[0m \u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m   1021\u001b[0m values \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_values\n\u001b[1;32m-> 1022\u001b[0m arr \u001b[38;5;241m=\u001b[39m \u001b[43mnp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43masarray\u001b[49m\u001b[43m(\u001b[49m\u001b[43mvalues\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m   1023\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m using_copy_on_write() \u001b[38;5;129;01mand\u001b[39;00m astype_is_view(values\u001b[38;5;241m.\u001b[39mdtype, arr\u001b[38;5;241m.\u001b[39mdtype):\n\u001b[0;32m   1024\u001b[0m     arr \u001b[38;5;241m=\u001b[39m arr\u001b[38;5;241m.\u001b[39mview()\n",
      "\u001b[1;31mValueError\u001b[0m: could not convert string to float: 'stayin in tonight... movie night... solo status '"
     ]
    }
   ],
   "source": [
    "SVCmodel = LinearSVC()\n",
    "SVCmodel.fit(X_train, y_train)\n",
    "model_Evaluate(SVCmodel)\n",
    "y_pred2 = SVCmodel.predict(X_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "cc1d34ec-716c-4e54-a280-27eec440ff40",
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'y_pred2' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[56], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01msklearn\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mmetrics\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m roc_curve, auc\n\u001b[1;32m----> 2\u001b[0m fpr, tpr, thresholds \u001b[38;5;241m=\u001b[39m roc_curve(y_test, \u001b[43my_pred2\u001b[49m)\n\u001b[0;32m      3\u001b[0m roc_auc \u001b[38;5;241m=\u001b[39m auc(fpr, tpr)\n\u001b[0;32m      4\u001b[0m plt\u001b[38;5;241m.\u001b[39mfigure()\n",
      "\u001b[1;31mNameError\u001b[0m: name 'y_pred2' is not defined"
     ]
    }
   ],
   "source": [
    "from sklearn.metrics import roc_curve, auc\n",
    "fpr, tpr, thresholds = roc_curve(y_test, y_pred2)\n",
    "roc_auc = auc(fpr, tpr)\n",
    "plt.figure()\n",
    "plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)\n",
    "plt.xlim([0.0, 1.0])\n",
    "plt.ylim([0.0, 1.05])\n",
    "plt.xlabel('False Positive Rate')\n",
    "plt.ylabel('True Positive Rate')\n",
    "plt.title('ROC CURVE')\n",
    "plt.legend(loc=\"lower right\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "03272e91-de0d-46a4-a2d2-c19fce59429b",
   "metadata": {},
   "outputs": [
    {
     "ename": "ValueError",
     "evalue": "could not convert string to float: 'stayin in tonight... movie night... solo status '",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mValueError\u001b[0m                                Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[57], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m LRmodel \u001b[38;5;241m=\u001b[39m LogisticRegression(C \u001b[38;5;241m=\u001b[39m \u001b[38;5;241m2\u001b[39m, max_iter \u001b[38;5;241m=\u001b[39m \u001b[38;5;241m1000\u001b[39m, n_jobs\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m-\u001b[39m\u001b[38;5;241m1\u001b[39m)\n\u001b[1;32m----> 2\u001b[0m \u001b[43mLRmodel\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mfit\u001b[49m\u001b[43m(\u001b[49m\u001b[43mX_train\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43my_train\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m      3\u001b[0m model_Evaluate(LRmodel)\n\u001b[0;32m      4\u001b[0m y_pred3 \u001b[38;5;241m=\u001b[39m LRmodel\u001b[38;5;241m.\u001b[39mpredict(X_test)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\base.py:1474\u001b[0m, in \u001b[0;36m_fit_context.<locals>.decorator.<locals>.wrapper\u001b[1;34m(estimator, *args, **kwargs)\u001b[0m\n\u001b[0;32m   1467\u001b[0m     estimator\u001b[38;5;241m.\u001b[39m_validate_params()\n\u001b[0;32m   1469\u001b[0m \u001b[38;5;28;01mwith\u001b[39;00m config_context(\n\u001b[0;32m   1470\u001b[0m     skip_parameter_validation\u001b[38;5;241m=\u001b[39m(\n\u001b[0;32m   1471\u001b[0m         prefer_skip_nested_validation \u001b[38;5;129;01mor\u001b[39;00m global_skip_validation\n\u001b[0;32m   1472\u001b[0m     )\n\u001b[0;32m   1473\u001b[0m ):\n\u001b[1;32m-> 1474\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43mfit_method\u001b[49m\u001b[43m(\u001b[49m\u001b[43mestimator\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43margs\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwargs\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\linear_model\\_logistic.py:1201\u001b[0m, in \u001b[0;36mLogisticRegression.fit\u001b[1;34m(self, X, y, sample_weight)\u001b[0m\n\u001b[0;32m   1198\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m   1199\u001b[0m     _dtype \u001b[38;5;241m=\u001b[39m [np\u001b[38;5;241m.\u001b[39mfloat64, np\u001b[38;5;241m.\u001b[39mfloat32]\n\u001b[1;32m-> 1201\u001b[0m X, y \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43m_validate_data\u001b[49m\u001b[43m(\u001b[49m\n\u001b[0;32m   1202\u001b[0m \u001b[43m    \u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1203\u001b[0m \u001b[43m    \u001b[49m\u001b[43my\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1204\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mcsr\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1205\u001b[0m \u001b[43m    \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43m_dtype\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1206\u001b[0m \u001b[43m    \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mC\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1207\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_large_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43msolver\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;129;43;01mnot\u001b[39;49;00m\u001b[43m \u001b[49m\u001b[38;5;129;43;01min\u001b[39;49;00m\u001b[43m \u001b[49m\u001b[43m[\u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mliblinear\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43msag\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43msaga\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m]\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1208\u001b[0m \u001b[43m\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m   1209\u001b[0m check_classification_targets(y)\n\u001b[0;32m   1210\u001b[0m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mclasses_ \u001b[38;5;241m=\u001b[39m np\u001b[38;5;241m.\u001b[39munique(y)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\base.py:650\u001b[0m, in \u001b[0;36mBaseEstimator._validate_data\u001b[1;34m(self, X, y, reset, validate_separately, cast_to_ndarray, **check_params)\u001b[0m\n\u001b[0;32m    648\u001b[0m         y \u001b[38;5;241m=\u001b[39m check_array(y, input_name\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124my\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mcheck_y_params)\n\u001b[0;32m    649\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 650\u001b[0m         X, y \u001b[38;5;241m=\u001b[39m \u001b[43mcheck_X_y\u001b[49m\u001b[43m(\u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43my\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mcheck_params\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    651\u001b[0m     out \u001b[38;5;241m=\u001b[39m X, y\n\u001b[0;32m    653\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m no_val_X \u001b[38;5;129;01mand\u001b[39;00m check_params\u001b[38;5;241m.\u001b[39mget(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mensure_2d\u001b[39m\u001b[38;5;124m\"\u001b[39m, \u001b[38;5;28;01mTrue\u001b[39;00m):\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\validation.py:1263\u001b[0m, in \u001b[0;36mcheck_X_y\u001b[1;34m(X, y, accept_sparse, accept_large_sparse, dtype, order, copy, force_all_finite, ensure_2d, allow_nd, multi_output, ensure_min_samples, ensure_min_features, y_numeric, estimator)\u001b[0m\n\u001b[0;32m   1258\u001b[0m         estimator_name \u001b[38;5;241m=\u001b[39m _check_estimator_name(estimator)\n\u001b[0;32m   1259\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[0;32m   1260\u001b[0m         \u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mestimator_name\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m requires y to be passed, but the target y is None\u001b[39m\u001b[38;5;124m\"\u001b[39m\n\u001b[0;32m   1261\u001b[0m     )\n\u001b[1;32m-> 1263\u001b[0m X \u001b[38;5;241m=\u001b[39m \u001b[43mcheck_array\u001b[49m\u001b[43m(\u001b[49m\n\u001b[0;32m   1264\u001b[0m \u001b[43m    \u001b[49m\u001b[43mX\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1265\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43maccept_sparse\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1266\u001b[0m \u001b[43m    \u001b[49m\u001b[43maccept_large_sparse\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43maccept_large_sparse\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1267\u001b[0m \u001b[43m    \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1268\u001b[0m \u001b[43m    \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1269\u001b[0m \u001b[43m    \u001b[49m\u001b[43mcopy\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mcopy\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1270\u001b[0m \u001b[43m    \u001b[49m\u001b[43mforce_all_finite\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mforce_all_finite\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1271\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_2d\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_2d\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1272\u001b[0m \u001b[43m    \u001b[49m\u001b[43mallow_nd\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mallow_nd\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1273\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_min_samples\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_min_samples\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1274\u001b[0m \u001b[43m    \u001b[49m\u001b[43mensure_min_features\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mensure_min_features\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1275\u001b[0m \u001b[43m    \u001b[49m\u001b[43mestimator\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mestimator\u001b[49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1276\u001b[0m \u001b[43m    \u001b[49m\u001b[43minput_name\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mX\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[0;32m   1277\u001b[0m \u001b[43m\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m   1279\u001b[0m y \u001b[38;5;241m=\u001b[39m _check_y(y, multi_output\u001b[38;5;241m=\u001b[39mmulti_output, y_numeric\u001b[38;5;241m=\u001b[39my_numeric, estimator\u001b[38;5;241m=\u001b[39mestimator)\n\u001b[0;32m   1281\u001b[0m check_consistent_length(X, y)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\validation.py:997\u001b[0m, in \u001b[0;36mcheck_array\u001b[1;34m(array, accept_sparse, accept_large_sparse, dtype, order, copy, force_all_finite, ensure_2d, allow_nd, ensure_min_samples, ensure_min_features, estimator, input_name)\u001b[0m\n\u001b[0;32m    995\u001b[0m         array \u001b[38;5;241m=\u001b[39m xp\u001b[38;5;241m.\u001b[39mastype(array, dtype, copy\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mFalse\u001b[39;00m)\n\u001b[0;32m    996\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 997\u001b[0m         array \u001b[38;5;241m=\u001b[39m \u001b[43m_asarray_with_order\u001b[49m\u001b[43m(\u001b[49m\u001b[43marray\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mxp\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mxp\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    998\u001b[0m \u001b[38;5;28;01mexcept\u001b[39;00m ComplexWarning \u001b[38;5;28;01mas\u001b[39;00m complex_warning:\n\u001b[0;32m    999\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\n\u001b[0;32m   1000\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mComplex data not supported\u001b[39m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;132;01m{}\u001b[39;00m\u001b[38;5;130;01m\\n\u001b[39;00m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;241m.\u001b[39mformat(array)\n\u001b[0;32m   1001\u001b[0m     ) \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mcomplex_warning\u001b[39;00m\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\sklearn\\utils\\_array_api.py:521\u001b[0m, in \u001b[0;36m_asarray_with_order\u001b[1;34m(array, dtype, order, copy, xp)\u001b[0m\n\u001b[0;32m    519\u001b[0m     array \u001b[38;5;241m=\u001b[39m numpy\u001b[38;5;241m.\u001b[39marray(array, order\u001b[38;5;241m=\u001b[39morder, dtype\u001b[38;5;241m=\u001b[39mdtype)\n\u001b[0;32m    520\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[1;32m--> 521\u001b[0m     array \u001b[38;5;241m=\u001b[39m \u001b[43mnumpy\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43masarray\u001b[49m\u001b[43m(\u001b[49m\u001b[43marray\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43morder\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43morder\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m    523\u001b[0m \u001b[38;5;66;03m# At this point array is a NumPy ndarray. We convert it to an array\u001b[39;00m\n\u001b[0;32m    524\u001b[0m \u001b[38;5;66;03m# container that is consistent with the input's namespace.\u001b[39;00m\n\u001b[0;32m    525\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m xp\u001b[38;5;241m.\u001b[39masarray(array)\n",
      "File \u001b[1;32m~\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\pandas\\core\\series.py:1022\u001b[0m, in \u001b[0;36mSeries.__array__\u001b[1;34m(self, dtype)\u001b[0m\n\u001b[0;32m    975\u001b[0m \u001b[38;5;250m\u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m    976\u001b[0m \u001b[38;5;124;03mReturn the values as a NumPy array.\u001b[39;00m\n\u001b[0;32m    977\u001b[0m \n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m   1019\u001b[0m \u001b[38;5;124;03m      dtype='datetime64[ns]')\u001b[39;00m\n\u001b[0;32m   1020\u001b[0m \u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m   1021\u001b[0m values \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_values\n\u001b[1;32m-> 1022\u001b[0m arr \u001b[38;5;241m=\u001b[39m \u001b[43mnp\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43masarray\u001b[49m\u001b[43m(\u001b[49m\u001b[43mvalues\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mdtype\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mdtype\u001b[49m\u001b[43m)\u001b[49m\n\u001b[0;32m   1023\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m using_copy_on_write() \u001b[38;5;129;01mand\u001b[39;00m astype_is_view(values\u001b[38;5;241m.\u001b[39mdtype, arr\u001b[38;5;241m.\u001b[39mdtype):\n\u001b[0;32m   1024\u001b[0m     arr \u001b[38;5;241m=\u001b[39m arr\u001b[38;5;241m.\u001b[39mview()\n",
      "\u001b[1;31mValueError\u001b[0m: could not convert string to float: 'stayin in tonight... movie night... solo status '"
     ]
    }
   ],
   "source": [
    "LRmodel = LogisticRegression(C = 2, max_iter = 1000, n_jobs=-1)\n",
    "LRmodel.fit(X_train, y_train)\n",
    "model_Evaluate(LRmodel)\n",
    "y_pred3 = LRmodel.predict(X_test)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "id": "6984e572-5f71-4703-9a57-5dbce6a4a06e",
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'y_pred3' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[58], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01msklearn\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mmetrics\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m roc_curve, auc\n\u001b[1;32m----> 2\u001b[0m fpr, tpr, thresholds \u001b[38;5;241m=\u001b[39m roc_curve(y_test, \u001b[43my_pred3\u001b[49m)\n\u001b[0;32m      3\u001b[0m roc_auc \u001b[38;5;241m=\u001b[39m auc(fpr, tpr)\n\u001b[0;32m      4\u001b[0m plt\u001b[38;5;241m.\u001b[39mfigure()\n",
      "\u001b[1;31mNameError\u001b[0m: name 'y_pred3' is not defined"
     ]
    }
   ],
   "source": [
    "from sklearn.metrics import roc_curve, auc\n",
    "fpr, tpr, thresholds = roc_curve(y_test, y_pred3)\n",
    "roc_auc = auc(fpr, tpr)\n",
    "plt.figure()\n",
    "plt.plot(fpr, tpr, color='darkorange', lw=1, label='ROC curve (area = %0.2f)' % roc_auc)\n",
    "plt.xlim([0.0, 1.0])\n",
    "plt.ylim([0.0, 1.05])\n",
    "plt.xlabel('False Positive Rate')\n",
    "plt.ylabel('True Positive Rate')\n",
    "plt.title('ROC CURVE')\n",
    "plt.legend(loc=\"lower right\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f9dd796e-76a7-41b6-a949-fd7588acce05",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}