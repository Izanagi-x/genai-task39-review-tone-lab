import streamlit as st
from inference import load_model, classify_review

st.set_page_config(page_title='Review Tone Lab', page_icon='💬', layout='centered')
st.title('Review Tone Lab')
st.write('Explore how a generative language model reads the tone of a short review.')

@st.cache_resource(show_spinner=False)
def resources():
    return load_model()

def clear_result():
    st.session_state.pop('result', None)

st.session_state.setdefault('review_input', 'I loved this helpful book.')
left, right = st.columns(2)
if left.button('Positive example'):
    st.session_state.review_input = 'I loved this helpful book.'
    clear_result()
if right.button('Negative example'):
    st.session_state.review_input = 'This was a terrible waste of time.'
    clear_result()
review = st.text_area('Your review', key='review_input', height=140,
                      max_chars=800, on_change=clear_result)
if st.button('Generate label', type='primary'):
    clear_result()
    try:
        if not review.strip():
            raise ValueError('Enter a short review first.')
        with st.spinner('Reading the review...'):
            st.session_state.result = classify_review(review, resources())
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error('The model could not finish this request. Please try again in a moment.')
result = st.session_state.get('result')
if result:
    st.subheader('Generated tone')
    if result['label'] == 'Positive':
        st.success('Positive')
    elif result['label'] == 'Negative':
        st.info('Negative')
    else:
        st.warning('The model did not return a clear positive or negative label.')
    st.caption(f"Generated in {result['seconds']:.2f} seconds after model loading.")
    with st.expander('Model output'):
        st.code(result['generated_text'], language=None)
st.caption('A small-model demonstration for short reviews. Mixed or ambiguous opinions can be difficult to classify.')
