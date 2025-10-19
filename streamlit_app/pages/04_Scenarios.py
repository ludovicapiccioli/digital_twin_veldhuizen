left, right = st.columns([3, 1.7], vertical_alignment="top")
with left:
    st.plotly_chart(fig, use_container_width=True)
with right:
    c1, c2 = st.columns(2)
    c1.metric("Δ Social", plus(d_social)); c2.metric("Δ Physical", plus(d_physical))
    c1.metric("Δ Safety", plus(d_safety));  st.metric("Δ QoL", plus(q_total))
    st.plotly_chart(g, use_container_width=True)
