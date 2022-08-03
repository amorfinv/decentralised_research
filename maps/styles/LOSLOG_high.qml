<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" styleCategories="AllStyleCategories" minScale="1e+08" version="3.22.3-Białowieża" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" mode="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option value="false" name="WMSBackgroundLayer" type="bool"/>
      <Option value="false" name="WMSPublishDataSourceUrl" type="bool"/>
      <Option value="0" name="embeddedWidgets/count" type="int"/>
      <Option value="Value" name="identify/format" type="QString"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour" enabled="false"/>
    </provider>
    <rasterrenderer opacity="1" classificationMin="0" nodataColor="" classificationMax="100" type="singlebandpseudocolor" alphaBand="-1" band="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="1" labelPrecision="4" colorRampType="INTERPOLATED" clip="0" minimumValue="0" maximumValue="100">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option value="68,1,84,191" name="color1" type="QString"/>
              <Option value="253,231,37,191" name="color2" type="QString"/>
              <Option value="0" name="discrete" type="QString"/>
              <Option value="gradient" name="rampType" type="QString"/>
              <Option value="0.0196078;70,8,92,191:0.0392157;71,16,99,191:0.0588235;72,23,105,191:0.0784314;72,29,111,191:0.0980392;72,36,117,191:0.117647;71,42,122,191:0.137255;70,48,126,191:0.156863;69,55,129,191:0.176471;67,61,132,191:0.196078;65,66,135,191:0.215686;63,72,137,191:0.235294;61,78,138,191:0.254902;58,83,139,191:0.27451;56,89,140,191:0.294118;53,94,141,191:0.313725;51,99,141,191:0.333333;49,104,142,191:0.352941;46,109,142,191:0.372549;44,113,142,191:0.392157;42,118,142,191:0.411765;41,123,142,191:0.431373;39,128,142,191:0.45098;37,132,142,191:0.470588;35,137,142,191:0.490196;33,142,141,191:0.509804;32,146,140,191:0.529412;31,151,139,191:0.54902;30,156,137,191:0.568627;31,161,136,191:0.588235;33,165,133,191:0.607843;36,170,131,191:0.627451;40,174,128,191:0.647059;46,179,124,191:0.666667;53,183,121,191:0.686275;61,188,116,191:0.705882;70,192,111,191:0.72549;80,196,106,191:0.745098;90,200,100,191:0.764706;101,203,94,191:0.784314;112,207,87,191:0.803922;124,210,80,191:0.823529;137,213,72,191:0.843137;149,216,64,191:0.862745;162,218,55,191:0.882353;176,221,47,191:0.901961;189,223,38,191:0.921569;202,225,31,191:0.941176;216,226,25,191:0.960784;229,228,25,191:0.980392;241,229,29,191" name="stops" type="QString"/>
            </Option>
            <prop k="color1" v="68,1,84,191"/>
            <prop k="color2" v="253,231,37,191"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.0196078;70,8,92,191:0.0392157;71,16,99,191:0.0588235;72,23,105,191:0.0784314;72,29,111,191:0.0980392;72,36,117,191:0.117647;71,42,122,191:0.137255;70,48,126,191:0.156863;69,55,129,191:0.176471;67,61,132,191:0.196078;65,66,135,191:0.215686;63,72,137,191:0.235294;61,78,138,191:0.254902;58,83,139,191:0.27451;56,89,140,191:0.294118;53,94,141,191:0.313725;51,99,141,191:0.333333;49,104,142,191:0.352941;46,109,142,191:0.372549;44,113,142,191:0.392157;42,118,142,191:0.411765;41,123,142,191:0.431373;39,128,142,191:0.45098;37,132,142,191:0.470588;35,137,142,191:0.490196;33,142,141,191:0.509804;32,146,140,191:0.529412;31,151,139,191:0.54902;30,156,137,191:0.568627;31,161,136,191:0.588235;33,165,133,191:0.607843;36,170,131,191:0.627451;40,174,128,191:0.647059;46,179,124,191:0.666667;53,183,121,191:0.686275;61,188,116,191:0.705882;70,192,111,191:0.72549;80,196,106,191:0.745098;90,200,100,191:0.764706;101,203,94,191:0.784314;112,207,87,191:0.803922;124,210,80,191:0.823529;137,213,72,191:0.843137;149,216,64,191:0.862745;162,218,55,191:0.882353;176,221,47,191:0.901961;189,223,38,191:0.921569;202,225,31,191:0.941176;216,226,25,191:0.960784;229,228,25,191:0.980392;241,229,29,191"/>
          </colorramp>
          <item value="0" alpha="191" label="0.0000" color="#440154"/>
          <item value="1.96078" alpha="191" label="1.9608" color="#46085c"/>
          <item value="3.92157" alpha="191" label="3.9216" color="#471063"/>
          <item value="5.88235" alpha="191" label="5.8823" color="#481769"/>
          <item value="7.84314" alpha="191" label="7.8431" color="#481d6f"/>
          <item value="9.803920000000002" alpha="191" label="9.8039" color="#482475"/>
          <item value="11.7647" alpha="191" label="11.7647" color="#472a7a"/>
          <item value="13.725499999999998" alpha="191" label="13.7255" color="#46307e"/>
          <item value="15.686300000000001" alpha="191" label="15.6863" color="#453781"/>
          <item value="17.6471" alpha="191" label="17.6471" color="#433d84"/>
          <item value="19.6078" alpha="191" label="19.6078" color="#414287"/>
          <item value="21.5686" alpha="191" label="21.5686" color="#3f4889"/>
          <item value="23.5294" alpha="191" label="23.5294" color="#3d4e8a"/>
          <item value="25.4902" alpha="191" label="25.4902" color="#3a538b"/>
          <item value="27.450999999999997" alpha="191" label="27.4510" color="#38598c"/>
          <item value="29.4118" alpha="191" label="29.4118" color="#355e8d"/>
          <item value="31.3725" alpha="191" label="31.3725" color="#33638d"/>
          <item value="33.3333" alpha="191" label="33.3333" color="#31688e"/>
          <item value="35.2941" alpha="191" label="35.2941" color="#2e6d8e"/>
          <item value="37.2549" alpha="191" label="37.2549" color="#2c718e"/>
          <item value="39.2157" alpha="191" label="39.2157" color="#2a768e"/>
          <item value="41.1765" alpha="191" label="41.1765" color="#297b8e"/>
          <item value="43.1373" alpha="191" label="43.1373" color="#27808e"/>
          <item value="45.098" alpha="191" label="45.0980" color="#25848e"/>
          <item value="47.0588" alpha="191" label="47.0588" color="#23898e"/>
          <item value="49.019600000000004" alpha="191" label="49.0196" color="#218e8d"/>
          <item value="50.9804" alpha="191" label="50.9804" color="#20928c"/>
          <item value="52.9412" alpha="191" label="52.9412" color="#1f978b"/>
          <item value="54.901999999999994" alpha="191" label="54.9020" color="#1e9c89"/>
          <item value="56.8627" alpha="191" label="56.8627" color="#1fa188"/>
          <item value="58.823499999999996" alpha="191" label="58.8235" color="#21a585"/>
          <item value="60.7843" alpha="191" label="60.7843" color="#24aa83"/>
          <item value="62.7451" alpha="191" label="62.7451" color="#28ae80"/>
          <item value="64.7059" alpha="191" label="64.7059" color="#2eb37c"/>
          <item value="66.6667" alpha="191" label="66.6667" color="#35b779"/>
          <item value="68.6275" alpha="191" label="68.6275" color="#3dbc74"/>
          <item value="70.5882" alpha="191" label="70.5882" color="#46c06f"/>
          <item value="72.54899999999999" alpha="191" label="72.5490" color="#50c46a"/>
          <item value="74.5098" alpha="191" label="74.5098" color="#5ac864"/>
          <item value="76.4706" alpha="191" label="76.4706" color="#65cb5e"/>
          <item value="78.4314" alpha="191" label="78.4314" color="#70cf57"/>
          <item value="80.3922" alpha="191" label="80.3922" color="#7cd250"/>
          <item value="82.35289999999999" alpha="191" label="82.3529" color="#89d548"/>
          <item value="84.3137" alpha="191" label="84.3137" color="#95d840"/>
          <item value="86.2745" alpha="191" label="86.2745" color="#a2da37"/>
          <item value="88.23530000000001" alpha="191" label="88.2353" color="#b0dd2f"/>
          <item value="90.1961" alpha="191" label="90.1961" color="#bddf26"/>
          <item value="92.1569" alpha="191" label="92.1569" color="#cae11f"/>
          <item value="94.1176" alpha="191" label="94.1176" color="#d8e219"/>
          <item value="96.0784" alpha="191" label="96.0784" color="#e5e419"/>
          <item value="98.03920000000001" alpha="191" label="98.0392" color="#f1e51d"/>
          <item value="100" alpha="191" label="100.0000" color="#fde725"/>
          <rampLegendSettings orientation="1" maximumLabel="" useContinuousLegend="1" suffix="" direction="0" minimumLabel="" prefix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option value="" name="decimal_separator" type="QChar"/>
                <Option value="6" name="decimals" type="int"/>
                <Option value="0" name="rounding_type" type="int"/>
                <Option value="false" name="show_plus" type="bool"/>
                <Option value="true" name="show_thousand_separator" type="bool"/>
                <Option value="false" name="show_trailing_zeros" type="bool"/>
                <Option value="" name="thousand_separator" type="QChar"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" gamma="1" contrast="0"/>
    <huesaturation invertColors="0" colorizeOn="0" saturation="0" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" grayscaleMode="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
